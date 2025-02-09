import {Prisma} from "@prisma/client";


export const useAuthentication = () => useState<boolean>("authenticated", () => false);
export const usePlayingSong = () => useState('playingSong', () => ({
    id: 0,
    elapsedTime: 0,
    totalTime: 0,
    waveformPeaks: null,
}));
// export const usePlayingSong = () => useState<Number>('id', () => 0)
