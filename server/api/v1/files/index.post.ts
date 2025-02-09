import {ServerFile} from "nuxt-file-storage";

export default defineEventHandler(async (event) => {
    const { files } = await readBody<{ files: ServerFile[] }>(event)
    const fileNames: string[] = []
    console.log('fileNames', fileNames)
    for (const file of files) {
        console.log(`file ${fileNames.join(' ')}`)
        console.log(file.content)

        const { binaryString, ext } = parseDataUrl(file.content)
        //? Extract the file extension from the original filename
        const originalExt = file.name.toString().split('.').pop() || ext
        const filename_stem = "file"
        const filename =  `${filename_stem}.${originalExt}`

        await useStorage('musicFiles').setItem(filename, binaryString.toString())
        const musicStorage = useStorage("musicFiles")

        // fileNames.push(await storeFileLocally(file, 12, '/specificFolder'))
    }
    return fileNames
})