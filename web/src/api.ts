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
  metadata: {
    duration?: number
    genre?: string
    year?: number
  }
}

export interface Api {
  getSongs(): Promise<Song[]>
  createSong(song: Omit<Song, 'id'>): Promise<Song>
  deleteSong(songId: string): Promise<void>
  uploadFile(file: File): Promise<Song>
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
      link: song.link  // Keep original link field
    }))
  },

  async createSong(song: Omit<Song, 'id'>): Promise<Song> {
    const { isDummy, url, ...rest } = song
    const response = await axios.post(`${API_BASE_URL}/api/songs/`, { 
      ...rest, 
      is_dummy: isDummy,
      link: url  // Map url to link for backend
    })
    return response.data
  },

  async deleteSong(songId: string): Promise<void> {
    await axios.delete(`${API_BASE_URL}/api/songs/${songId}/`)
  },

  async uploadFile(file: File): Promise<Song> {
    const formData = new FormData()
    formData.append('file', file)
    const response = await axios.post(`${API_BASE_URL}/api/upload/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  }
} 