import prisma from '~/lib/prisma';
import {promises as fs} from 'fs';
import path from 'path';
import {parseBlob} from 'music-metadata';

export default defineEventHandler(async (event) => {
    const formData = await readFormData(event);
    const file = formData.get('file') as File | null;

    if (!file) {
        throw createError({statusCode: 400, statusMessage: 'No file found in upload'});
    }

    let metadata;
    try {
        metadata = await parseBlob(file);
    } catch (err: any) {
        throw createError({statusCode: 400, statusMessage: `${err.message} is not a valid audio file`});
    }

    const title = metadata.common.title || '';
    const artist = metadata.common.artist || '';
    const album = metadata.common.album || '';
    const genre = (metadata.common.genre && metadata.common.genre.join(', ')) || '';

    const filePath = path.join(DATA_PATH, file.name);

    const arrayBuffer = await file.arrayBuffer();
    await fs.writeFile(filePath, Buffer.from(arrayBuffer));
    await transcodeSong(filePath);

    let createdSong;
    createdSong = await prisma.song.create({
        data: {
            title: title,
            artists: artist,
            album: album,
            genre: genre,
            label: 'Unknown',
            path: filePath,
            localy_stored: true,
        },
    });

    return createdSong;
});
