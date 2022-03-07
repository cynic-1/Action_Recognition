import db from "../models/index.js"
const Video = db.video;
const User = db.user;
import multer from 'multer'
import path from 'path'
import fs from 'fs'
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

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
    const id = req.body.id;
    const video = new Video({
        name: req.file.filename,
        uploader: id,
        raw: req.file.path
    });
    video
        .save(video)
        .then(data => {
            User.findByIdAndUpdate(id,
                {$push: {videos: data._id}})
                .then(() => {
                    res.send(req.file);
                })
                .catch(err => {
                    res.status(500).send({
                        message:
                            err.message || "user id is invalid."
                    });
                })
        })
        .catch(err => {
            res.status(500).send({
                message:
                    err.message || "Some error occurred while storing the video."
            });
        })
}

export const getVideo = (req, res) => {
        const vid = req.params.id;
        Video.findById(vid)
            .then(data => {
                let videoPath = path.resolve(__dirname, '../../'+data.raw)

                let readStream = fs.createReadStream(videoPath)

                readStream.pipe(res);
            })
            .catch(err => {
                res.status(500).send({
                    message:
                        err.message || "Some error occurred while storing the video."
                });
            })
}

export const getVideoChunk = function(req, res) {
    const vid = req.params.id;
    Video.findById(vid)
        .then(data => {
            const videoPath = path.resolve(__dirname, '../../' + data.raw)
            const stat = fs.statSync(videoPath)
            const fileSize = stat.size
            const range = req.headers.range
            if (range) {
                const parts = range.replace(/bytes=/, "").split("-")
                const start = parseInt(parts[0], 10)
                const end = parts[1]
                    ? parseInt(parts[1], 10)
                    : fileSize-1
                const chunksize = (end-start)+1
                const file = fs.createReadStream(videoPath, {start, end})
                const head = {
                    'Content-Range': `bytes ${start}-${end}/${fileSize}`,
                    'Accept-Ranges': 'bytes',
                    'Content-Length': chunksize,
                    'Content-Type': 'video/mp4',
                }
                res.writeHead(206, head);
                file.pipe(res);
            } else {
                const head = {
                    'Content-Length': fileSize,
                    'Content-Type': 'video/mp4',
                }
                res.writeHead(200, head)
                fs.createReadStream(videoPath).pipe(res)
            }
        })
        .catch(err => {
            res.status(500).send({
                message:
                    err.message || "Some error occurred while storing the video."
            });
        })
}

export const getKeyPoints = (req, res) => {
    const id = req.params.id
    Video.findById(id)
        .populate('keyPoints')
        .then(data => {
            res.send(data)
        })
        .catch(err => {
            res.status(500).send({
                message:
                    err.message || "Some error occurred while fetching keyPoints."
            });
        })
}
