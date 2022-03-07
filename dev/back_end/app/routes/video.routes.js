import {Router} from 'express'
import * as video from "../controller/video.controller.js"

export default app => {
    const router = Router()
    // Upload a video
    router.post("/upload", video.videoUpload.single('video'), video.store, (req, res) => {
        res.status(400).send({ error: "Error!!!" })
    });
    router.get('/:id', video.getVideo)
    router.get('/:id/keyPoints', video.getKeyPoints)
    app.use('/api/videos', router);
};
