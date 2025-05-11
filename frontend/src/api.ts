import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

export interface Song {
  id: string
  title: string
  artist: string
  isDummy: number  // 0 for real songs, 1 for dummy songs
  filePath?: string
  url?: string
  link?: string  // Add link field to match backend
  album?: string  // Add album field to match backend
  metadata: {
    duration?: number
    genre?: string
    year?: number
  }
}

export interface UploadResult {
  uploaded_songs: Song[]
  errors: {
    filename: string
    error: string
    message: string
    existing_song?: {
      id: string
      title: string
      artist: string
    }
  }[]
}

export interface Api {
  getSongs(): Promise<Song[]>
  createSong(song: Omit<Song, 'id'>): Promise<Song>
  deleteSong(songId: string): Promise<void>
  uploadFiles(files: File[]): Promise<UploadResult>
}

export const api: Api = {
  // Songs
  async getSongs(): Promise<Song[]> {
    const response = await axios.get(`${API_BASE_URL}/api/songs/`)
    return response.data.map((song: any) => ({
      ...song,
      isDummy: song.is_dummy,
      filePath: song.file_path,
      url: song.link,  // Map link to url for frontend
      link: song.link,  // Keep original link field
      metadata: {
        duration: song.duration,
        genre: song.genre,
        year: song.year
      }
    }))
  },

  async createSong(song: Omit<Song, 'id'>): Promise<Song> {
    const { isDummy, url, metadata, ...rest } = song
    const response = await axios.post(`${API_BASE_URL}/api/songs/`, { 
      ...rest, 
      is_dummy: isDummy,
      link: url,  // Map url to link for backend
      duration: metadata?.duration,
      genre: metadata?.genre,
      year: metadata?.year
    })
    return response.data
  },

  async deleteSong(songId: string): Promise<void> {
    await axios.delete(`${API_BASE_URL}/api/songs/${songId}/`)
  },

  async uploadFiles(files: File[]): Promise<UploadResult> {
    const formData = new FormData()
    files.forEach(file => {
      formData.append('files', file)
    })
    const response = await axios.post(`${API_BASE_URL}/api/upload/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          // Emit progress event
          window.dispatchEvent(new CustomEvent('upload-progress', {
            detail: {
              progress: percentCompleted
            }
          }))
        }
      }
    })
    return {
      ...response.data,
      uploaded_songs: response.data.uploaded_songs.map((song: any) => ({
        ...song,
        isDummy: song.is_dummy,
        filePath: song.file_path,
        url: song.link,
        link: song.link,
        metadata: {
          duration: song.duration,
          genre: song.genre,
          year: song.year
        }
      }))
    }
  }
} 