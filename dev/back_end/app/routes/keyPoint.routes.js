import {Router} from 'express'
import * as keyPoint from "../controller/keyPoint.controller.js"

export default app => {
    const router = Router()
    // Upload a video
    router.get('/:id/image', keyPoint.getImage)
    app.use('/api/keyPoints', router);
};
