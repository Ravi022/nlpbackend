// require("dotenv").config({ path: "./env" }); method first to use .env file.
import dotenv from "dotenv";
import mongoose, { connect } from "mongoose";
// import { DB_NAME } from "./constants.js";
// import { listen } from "express/lib/application";
import { connectDB } from "./db/db.js";
import { app } from "./server.js";

dotenv.config({ path: "./.env" });

connectDB()
  .then(() => {
    app.listen(process.env.PORT || 8000, () => {
      console.log(`server is running at port : ${process.env.PORT}`);
    });
  })
  .catch((error) => {
    console.log("MongoDB connection failed :", error);
  });
