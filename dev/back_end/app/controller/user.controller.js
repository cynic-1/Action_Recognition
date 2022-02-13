import db from "../models/index.js"
const User = db.user;
import sha256 from 'crypto-js/sha256.js';
// Create and Save a new user
export const create = (req, res) => {
    // Validate request
    if (!(req.body.identity !== undefined && req.body.id && req.body.name && req.body.college && req.body.pwd)) {
        res.status(400).send({ message: "Content can not be empty!" });
        return;
    }
    // Create a User
    const user = new User({
        identity: req.body.identity,
        id: req.body.id,
        name: req.body.name,
        college: req.body.college,
        mail: req.body.mail || "",
        pwd: sha256(req.body.pwd)
    });
    // Save User in the database
    user
        .save(user)
        .then(data => {
            res.send(data);
        })
        .catch(err => {
            res.status(500).send({
                message:
                    err.message || "Some error occurred while creating the User."
            });
        });
}
export const logIn = (req, res) => {
    const id = req.body.id;
    User.findOne(id ? { id: { $regex: new RegExp(id), $options: "i" } } : {})
        .then(data => {
            if (data.pwd === sha256(req.body.pwd).toString()) {
                // res.send("login success!")
                res.send(data);
            } else {
                res.status(800).send({
                    message:
                        data.pwd + " " + req
                });
            }
            // res.send(data)
        })
        .catch(err => {
            res.status(500).send({
                message:
                    err.message || "Some error occurred while retrieving users."
            });
        })
}
// Retrieve all Users from the database by the name.
export const findAllByName = (req, res) => {
    const name = req.query.name;
    let condition = name ? { name: { $regex: new RegExp(name), $options: "i" } } : {};
    User.find(condition)
        .then(data => {
            res.send(data);
        })
        .catch(err => {
            res.status(500).send({
                message:
                    err.message || "Some error occurred while retrieving users."
            });
        });
}
// Find a single User with an id
export const findById = (req, res) => {
    const id = req.params.id;
    User.findById(id)
        .then(data => {
            if (!data)
                res.status(404).send({ message: "Not found user with id " + id });
            else res.send(data);
        })
        .catch(() => {
            res
                .status(500)
                .send({ message: "Error retrieving user with id=" + id });
        });
}
// Update a user by the id in the request
export const updateById = (req, res) => {
    if (!req.body) {
        return res.status(400).send({
            message: "Data to update can not be empty!"
        });
    }
    const id = req.params.id;
    User.findByIdAndUpdate(id, req.body, { useFindAndModify: false })
        .then(data => {
            if (!data) {
                res.status(404).send({
                    message: `Cannot update user with id=${id}. Maybe User was not found!`
                });
            } else res.send({ message: "User was updated successfully." });
        })
        .catch(() => {
            res.status(500).send({
                message: "Error updating user with id=" + id
            });
        });
}
// Delete a User with the specified id in the request
export const deleteById = (req, res) => {
    const id = req.params.id;
    User.findByIdAndRemove(id)
        .then(data => {
            if (!data) {
                res.status(404).send({
                    message: `Cannot delete user with id=${id}. Maybe user was not found!`
                });
            } else {
                res.send({
                    message: "User was deleted successfully!"
                });
            }
        })
        .catch(() => {
            res.status(500).send({
                message: "Could not delete user with id=" + id
            });
        });
}

