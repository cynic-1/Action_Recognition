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
                teachers: data,
                students: req.body.students || [],
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

