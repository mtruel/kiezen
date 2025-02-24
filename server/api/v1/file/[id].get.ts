import prisma from '~/lib/prisma';
import {promises as fs} from 'fs';
import path from 'path';
import {createReadStream} from "node:fs";

export default defineEventHandler(async (event) => {
    const id = getRouterParam(event, 'id')
    const song = await prisma.song.findUnique({where: {id: Number(id)}});

    if (!song) {
        throw createError({statusCode: 404, statusMessage: 'Song not found'});
    }
    if (!song.path) {
        throw createError({ statusCode: 400, statusMessage: 'Song path is missing' });
    }

    const originalPath = path.join(DATA_PATH, song.path);
    console.log(originalPath);

    let transcodedPath = getTranscodingPath(originalPath);
    try {
        await fs.access(transcodedPath);
    } catch {
        // File does not exist –  transcoding
        transcodedPath = await transcodeSong(originalPath);
    }

    const fileStream = createReadStream(transcodedPath);
    setHeader(event, 'Content-Type', 'audio/mpeg');
    setHeader(event, 'Content-Disposition', `attachment; filename="${path.basename(originalPath)}"`);
    return sendStream(event, fileStream);
});
