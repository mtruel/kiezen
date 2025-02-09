import prisma from "~/lib/prisma";

export default defineEventHandler(async (event) => {
    return prisma.song.findMany();
})