import {Router} from 'express'
import * as user from "../controller/user.controller.js"

export default app => {
    const router = Router()
    // Create a new User
    router.post("/", user.create);
    // Retrieve all Users
    router.get("/", user.findAllByName);
    // Retrieve a single User with id
    router.get("/:id", user.findById);
    // Update a Tutorial with id
    router.put("/:id", user.updateById);
    // Delete a Tutorial with id
    router.delete("/:id", user.deleteById);
    // Create a new Tutorial
    app.use('/api/user', router);
};
