import prisma from "~/lib/prisma";

export default defineEventHandler(async (event) => {
    const id = Number(getRouterParam(event, 'id'))
    console.log("API call song ", id);
    return prisma.song.findUnique({where: {id}});
})