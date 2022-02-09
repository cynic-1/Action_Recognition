import {Router} from 'express'
import * as course from "../controller/course.controller.js"

export default app => {
    const router = Router()
    // Create a new User
    router.post("/", course.create);
    app.use('/api/course', router);
};
