import { promises as fs } from 'fs'
import path from 'path'
import { spawn } from 'child_process'

export const DATA_PATH = '/home/mathias/WebstormProjects/kiezen/tmp'
export const TRANSCODING_PATH = path.join(DATA_PATH, 'transcriptions')

export function getTranscodingPath(originalPath: string, transcodeDir = TRANSCODING_PATH): string {
    const basename = path.basename(originalPath, path.extname(originalPath))
    return path.join(transcodeDir, `${basename}.ogg`)
}

export function transcodeSong(originalPath: string, transcodeDir = TRANSCODING_PATH): Promise<string> {
    return new Promise(async (resolve, reject) => {
        try {
            await fs.mkdir(transcodeDir, { recursive: true })
            const outputPath = getTranscodingPath(originalPath, transcodeDir)
            const args = ['-i', originalPath, '-y', outputPath]
            const ffmpeg = spawn('ffmpeg', args)
            let stderr = ''
            ffmpeg.stderr.on('data', (data) => { stderr += data.toString() })
            ffmpeg.on('close', (code) => {
                if (code !== 0) {
                    return reject(new Error(`Transcoding failed: ${stderr}`))
                }
                resolve(outputPath)
            })
        } catch (err) {
            reject(err)
        }
    })
}
