const express = require("express");
const ejs = require("ejs");
const path = require("path");
const bodyParser = require('body-parser');
const GoogleStrategy = require('passport-google-oauth20').Strategy;

const app = express();
app.use(express.static('public'))
app.set("views",path.join(__dirname,"views"));
app.set("view engine","ejs");
app.use(bodyParser.urlencoded({ extended: true }));


app.get("/",function(req,res){
    res.render("home")
})
app.get("/register",function(req,res){
    res.render("register")
})
app.get("/:customListName",function(req,res){
    const customListName = req.params.customListName;
    res.send("Welcome"+" "+customListName);
});
app.get("/:customListName/:customListName1/:customListName2",function(req,res){
    const customListName = req.params.customListName;
    const customListName1 = req.params.customListName1;
    const customListName2 = req.params.customListName2;
    res.render("lsm",{library:customListName1+" "+customListName2})
});

app.listen(3000),function(){
    console.log("Server started on port 3000");
};