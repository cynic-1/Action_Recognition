import db from "../models/index.js"

const Course = db.course;
// const User = db.user;

// Create and Save a new course
export const create = (req, res) => {
    // Validate request
    if (!(req.body.year && req.body.semester && req.body.name && req.body.teachers)) {
        res.status(400).send({ message: "Content can not be empty!" });
        return;
    }
    // Create a course
    const course = new Course({
        year: req.body.year,
        semester: req.body.semester,
        name: req.body.name,
        teachers: req.body.teachers
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
}

// Find a single course with an id
export const findById = (req, res) => {
    const id = req.params.id;
    Course.findById(id)
        .then(data => {
            if (!data)
                res.status(404).send({ message: "Not found course with _id " + id });
            else res.send(data);
        })
        .catch(() => {
            res
                .status(500)
                .send({ message: "Error retrieving course with _id=" + id });
        });
}

export const deleteById = (req, res) => {
    const id = req.params.id;
    Course.findByIdAndDelete(id)
        .then(data => {
            if (!data) {
                res.status(404).send({
                    message: `Cannot delete course with id=${id}. Maybe course was not found!`
                });
            } else {
                res.send({
                    message: "Course was deleted successfully!"
                });
            }
        })
        .catch(() => {
            res.status(500).send({
                message: "Could not delete course with id=" + id
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
    const id = req.params.id;
    Course.findByIdAndUpdate(id, req.body, { useFindAndModify: false })
        .then(data => {
            if (!data) {
                res.status(404).send({
                    message: `Cannot update course with id=${id}. Maybe course was not found!`
                });
            } else res.send({ message: "Course was updated successfully." });
        })
        .catch(() => {
            res.status(500).send({
                message: "Error updating course with id=" + id
            });
        });
}

export const getStudents = (req, res) => {
    const id = req.params.id;
    Course.findById(id)
        .populate('students')
        .then(data => {
            res.send(data.students)
        })
        .catch(() => {
            res.status(500).send({
                message: "Error getting students who attend the course with id=" + id
            });
        });
}

export const insertStudents = (req, res) => {
    const id = req.params.id;
    const _ids = req.body._ids;
    Course.findByIdAndUpdate(id, {$addToSet: {students: { $each: _ids }}})
        .then(data => {
            if (!data) {
                res.status(404).send({
                    message: `Cannot update course with id=${id}. Maybe course was not found!`
                });
            } else res.send({ message: "Course was updated successfully." });
        })
        .catch(() => {
            res.status(500).send({
                message: "Error updating course with id=" + id
            });
        });
}
