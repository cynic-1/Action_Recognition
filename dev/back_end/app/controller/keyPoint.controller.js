import db from "../models/index.js"
const Video = db.video;
const KeyPoint = db.keyPoint;
import multer from 'multer'
import path from 'path'
// import fs from 'fs'
import { fileURLToPath } from 'url';
// import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
// const __dirname = dirname(__filename);

const imageStorage = multer.diskStorage({
    destination: 'images', // Destination to store video
    filename: (req, file, cb) => {
        cb(null, file.fieldname + '_' + Date.now()
            + path.extname(file.originalname))
    }
});

export const imageUpload = multer({
    storage: imageStorage,
    limits: {
        fileSize: 1000000 // 1000000 Bytes = 1 MB
    },
    fileFilter(req, file, cb) {
        if (!file.originalname.match(/\.(png|jpg)$/)) {
            // upload only png and jpg format
            return cb(new Error('Please upload a Image'))
        }
        cb(undefined, true)
    }
})

export const store = (req, res) => {
    const id = req.params.vid;
    const keyPoint = new KeyPoint({
        imgLoc: req.file.path,
        data: req.body.data
    });
    keyPoint
        .save(keyPoint)
        .then(data => {
            Video.findByIdAndUpdate(id,
                {$push: {keyPoints: data._id}})
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

export const getKeyPoints = (req, res) => {
    const kid = req.params.kid;
    KeyPoint.findById(kid)
        .then(data => {
            // let imgPath = path.resolve(__dirname, '../../'+data.raw)
            //
            // let readStream = fs.createReadStream(videoPath)

            // readStream.pipe(res);
            res.send(data)
        })
        .catch(err => {
            res.status(500).send({
                message:
                    err.message || "Some error occurred while storing the video."
            });
        })

}

