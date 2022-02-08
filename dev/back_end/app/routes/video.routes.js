import {Router} from 'express'
import * as video from "../controller/video.controller.js"

export default app => {
    const router = Router()
    // Upload a video
    router.post("/upload", video.videoUpload.single('video'), video.store, (error, req, res, next) => {
        res.status(400).send({ error: error.message })
    });
    router.get('/get', video.getVideo)
    app.use('/api/video', router);
};
