import db from "../models/index.js"
const Video = db.video;
import multer from 'multer'
import path from 'path'

const videoStorage = multer.diskStorage({
    destination: 'videos', // Destination to store video
    filename: (req, file, cb) => {
        cb(null, file.fieldname + '_' + Date.now()
            + path.extname(file.originalname))
    }
});

export const videoUpload = multer({
    storage: videoStorage,
    limits: {
        fileSize: 1000000000 // 1000000000 Bytes = 1 GB
    },
    fileFilter(req, file, cb) {
        // upload only mp4 and mkv format
        if (!file.originalname.match(/\.(mp4|MPEG-4|mkv)$/)) {
            return cb(new Error('Please upload a video'))
        }
        cb(undefined, true)
    }
})

export const store = (req, res) => {
    const video = new Video({
        name: req.file.filename,
        raw: req.file.path
    });
    video
        .save(video)
        .then(() => {
            res.send(req.file);
        })
        .catch(err => {
            res.status(500).send({
                message:
                    err.message || "Some error occurred while storing the video."
            });
        })
}

export const findVideoById = (req, res) => {
    Video.findById(req.params.id)
}
