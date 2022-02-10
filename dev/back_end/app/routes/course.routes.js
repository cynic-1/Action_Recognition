import {Router} from 'express'
import * as course from "../controller/course.controller.js"

export default app => {
    const router = Router()
    // Create a new course
    router.post("/", course.create);
    // Retrieve a single User with id
    router.get("/:id", course.findById);
    // Update a User with id
    router.put("/:id", course.updateById);
    // delete a course by id
    router.delete("/:id", course.deleteById)
    app.use('/api/course', router);
};
