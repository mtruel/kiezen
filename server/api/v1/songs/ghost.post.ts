import prisma from '~/lib/prisma';
import {readBody} from 'h3';

export default defineEventHandler(async (event) => {
    const song = await readBody(event);
    return prisma.song.create({data: song});
});
