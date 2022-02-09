import db from "../models/index.js"

const Course = db.course;
const User = db.user;

// Create and Save a new course
export const create = (req, res) => {
    // Validate request
    if (!(req.body.year && req.body.semester && req.body.name && req.body.teachers)) {
        res.status(400).send({ message: "Content can not be empty!" });
        return;
    }
    User.find({
        'type': 1,
        'id': {$in: req.body.teachers}
    })
        .select('_id')
        .then(data => {
            // Create a course
            const course = new Course({
                year: req.body.year,
                semester: req.body.semester,
                name: req.body.name,
                teachers: data
                // students: req.body.students || [],
            });
            // Save User in the database
            course
                .save(course)
                .then(data => {
                    res.send(data);
                })
                .catch(err => {
                    res.status(500).send({
                        message:
                            err.message || "Some error occurred while creating the course."
                    });
                });
        })
        .catch(() => {
            res.status(400).send({ message: "No such teacher!" });
        })
}

export const deleteById = (req, res) => {
    const _id = req.params._id;
    Course.findByIdAndDelete(_id)
        .then(data => {
            if (!data) {
                res.status(404).send({
                    message: `Cannot delete course with id=${_id}. Maybe Tutorial was not found!`
                });
            } else {
                res.send({
                    message: "Course was deleted successfully!"
                });
            }
        })
        .catch(err => {
            res.status(500).send({
                message: "Could not delete course with id=" + _id
            });
        });
}

// Update a course by the id in the request
export const updateById = (req, res) => {
    if (!req.body) {
        return res.status(400).send({
            message: "Data to update can not be empty!"
        });
    }
    const _id = req.params._id;
    User.findByIdAndUpdate(_id, req.body, { useFindAndModify: false })
        .then(data => {
            if (!data) {
                res.status(404).send({
                    message: `Cannot update course with _id=${_id}. Maybe User was not found!`
                });
            } else res.send({ message: "Course was updated successfully." });
        })
        .catch(err => {
            res.status(500).send({
                message: "Error updating course with _id=" + _id
            });
        });
}

export const getStudents = (req, res) => {
    const _id = req.params._id;
    Course.findById(_id)
        .populate('students')
        .then(data => {
            res.send(data.students)
        })
        .catch(err => {
            res.status(500).send({
                message: "Error getting students who attend the course with _id=" + _id
            });
        });
}

export const insertStudents = (req, res) => {
    const _id = req.params._id;
    const sid = req.body.sid;
    Course.findByIdAndUpdate(_id, {$addToSet: {students: { $each: sid }}})
        .then(data => {
            if (!data) {
                res.status(404).send({
                    message: `Cannot update course with _id=${_id}. Maybe User was not found!`
                });
            } else res.send({ message: "Course was updated successfully." });
        })
        .catch(err => {
            res.status(500).send({
                message: "Error updating course with _id=" + _id
            });
        });
}
