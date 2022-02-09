// const dbConfig = require("../config/db.config.js");
import {url} from '../config/db.config.js'
import mongoose from 'mongoose'
import userModel from "./user.model.js";
import videoModel from "./video.model.js";
import courseModel from "./course.model.js";

mongoose.Promise = global.Promise;

const db = {};
db.mongoose = mongoose;
db.url = url;
db.user = userModel(mongoose);
db.video = videoModel(mongoose);
db.course = courseModel(mongoose);

export default db;
