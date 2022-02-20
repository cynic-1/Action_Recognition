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
    const {year, semester, name, teachers, day, classNo} = req.body
    // Create a course
    const course = new Course({ // cannot use word 'class', so replace it with classNo
        year,
        semester,
        name,
        teachers,
        day,
        classNo
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
    const id = req.params.id;// course id
    const _ids = req.body._ids; // student _id
    Course.findByIdAndUpdate(id, {$addToSet: {students: { $each: _ids }}})
        .then(data => {
            if (!data) {
                res.status(404).send({
                    message: `Cannot update course with id=${id}. Maybe course was not found!`
                });
            }
            // else res.send({ message: "Course was updated successfully." });
        })
        .catch(() => {
            res.status(500).send({
                message: "Error updating course with id=" + id
            });
        });
    _ids.forEach(v => {
        User.findByIdAndUpdate(v, {$push: {courses: id}})
            .catch(() => {
                res.status(500).send({
                    message: "Error insert student with _id=" + id
                });
            })
    })
    res.send({ message: "Course was updated successfully." });
}

export const findByTeacher = (req, res) => {
    const tid = req.query.teacher;
    Course.find({teachers: {$elemMatch: {$eq: tid}}})
        .then(data => {
            if (!data) {
                res.status(404).send({
                    message: `Cannot update course with id=${id}. Maybe course was not found!`
                });
            } else res.send(data);
        })
        .catch(() => {
            res.status(500).send({
                message: "Error updating course with id=" + id
            });
        });
}
