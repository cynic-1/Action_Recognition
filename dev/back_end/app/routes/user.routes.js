import {Router} from 'express'
import * as user from "../controller/user.controller.js"
import * as video from "../controller/video.controller.js";

export default app => {
    const router = Router()
    // Create a new User
    router.post("/", user.create);
    // Retrieve all Users
    router.get("/", user.findAllByName);
    router.get("/:id/videos", user.findVideosByUser)
    router.post("/login", user.logIn);
    // Retrieve a single User with id
    router.get("/:id", user.findById);
    // Update a User with id
    router.put("/:id", user.updateById);
    // Delete a User with id
    router.delete("/:id", user.deleteById);
    router.post("/:id/avatar/upload", user.imageUpload.single('img'), user.store, (req, res) => {
        res.status(400).send({ error: "Error!!!" })
    });

    app.use('/api/user', router);
};
