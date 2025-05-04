import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

export interface Song {
  id: string
  title: string
  artist: string
  isDummy: boolean
  filePath?: string
  url?: string
  metadata: {
    duration?: number
    genre?: string
    year?: number
  }
}

export const api = {
  // Songs
  async getSongs(): Promise<Song[]> {
    const response = await axios.get(`${API_BASE_URL}/api/songs/`)
    return response.data
  },

  async createSong(song: Omit<Song, 'id'>): Promise<Song> {
    const response = await axios.post(`${API_BASE_URL}/api/songs/`, song)
    return response.data
  },

  async deleteSong(songId: string): Promise<void> {
    await axios.delete(`${API_BASE_URL}/api/songs/${songId}/`)
  }
} 