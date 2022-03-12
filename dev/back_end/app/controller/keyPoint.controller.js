import db from "../models/index.js"
const Video = db.video;
const KeyPoint = db.keyPoint;
import multer from 'multer'
import path from 'path'
import { fileURLToPath } from 'url';
import fs from "fs";
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// const imageStorage = multer.diskStorage({
//     destination: 'images', // Destination to store video
//     filename: (req, file, cb) => {
//         cb(null, file.fieldname + '_' + Date.now()
//             + path.extname(file.originalname))
//     }
// });
//
// export const imageUpload = multer({
//     storage: imageStorage,
//     limits: {
//         fileSize: 1000000 // 1000000 Bytes = 1 MB
//     },
//     fileFilter(req, file, cb) {
//         if (!file.originalname.match(/\.(png|jpg)$/)) {
//             // upload only png and jpg format
//             return cb(new Error('Please upload a Image'))
//         }
//         cb(undefined, true)
//     }
// })
//
// export const store = (req, res) => {
//     const id = req.params.vid;
//     const keyPoint = new KeyPoint({
//         imgLoc: req.file.path,
//         data: req.body.data
//     });
//     keyPoint
//         .save(keyPoint)
//         .then(data => {
//             Video.findByIdAndUpdate(id,
//                 {$push: {keyPoints: data._id}})
//                 .then(() => {
//                     res.send(req.file);
//                 })
//                 .catch(err => {
//                     res.status(500).send({
//                         message:
//                             err.message || "user id is invalid."
//                     });
//                 })
//         })
//         .catch(err => {
//             res.status(500).send({
//                 message:
//                     err.message || "Some error occurred while storing the video."
//             });
//         })
// }

export const getImage = (req, res) => {
    const id = req.params.id;
    KeyPoint.findById(id)
        .then(data => {
            let imagePath = path.resolve(__dirname, '../../images/keyPoints/'+data.imgLoc)

            fs.readFile(imagePath, 'binary', (err, file) => {
                if (err) {
                    res.status(500).send({
                        message:
                            err.message || "Some error occurred while storing the video."
                    });
                    return
                }
                res.writeHead(200, {'Content-Type': 'image/jpeg'})
                res.write(file, 'binary')
                res.end()
            })
        })
        .catch(err => {
            res.status(500).send({
                message:
                    err.message || "Some error occurred while storing the video."
            });
        })
}

