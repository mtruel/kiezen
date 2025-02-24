import prisma from '~/lib/prisma';

export default defineEventHandler(async (event) => {
    const id = getRouterParam(event, 'id')
    return prisma.song.findUnique({where: {id: Number(id)}});
});
