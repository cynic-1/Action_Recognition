import {Router} from 'express'
import {store, videoUpload} from "../controller/video.controller.js"

export default app => {
    const router = Router()
    // Upload a video
    router.post("/upload", videoUpload.single('video'), store, (error, req, res, next) => {
        res.status(400).send({ error: error.message })
    });
    app.use('/api/video', router);
};
