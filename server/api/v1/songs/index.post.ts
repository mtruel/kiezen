import prisma from "~/lib/prisma";

export default defineEventHandler(async (event) => {
    const data = getRouterParam(event, 'data');
    return await prisma.song.create({
        data: {data}
    })
})