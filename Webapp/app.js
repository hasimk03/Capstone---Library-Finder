require("dotenv").config();
const express = require("express");
const ejs = require("ejs");
const path = require("path");
const bodyParser = require('body-parser');
const passport = require('passport');
const session = require('express-session');
const cookieSession = require('cookie-session');
const GoogleStrategy = require('passport-google-oauth20').Strategy;

require('./config/passport-setup')

const app = express();

app.use(express.static('public'));

app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");
app.use(bodyParser.urlencoded({ extended: true }));

app.use(session({
  secret: process.env.SECRET,
  resave: false,
  saveUninitialized: false
}));

app.use(passport.initialize());
app.use(passport.session());

// Route for initiating Google OAuth2 authentication
app.get('/google', passport.authenticate('google', {
  scope: ['profile', 'email']
}));

// Route for handling Google OAuth2 callback
app.get('/google/callback', passport.authenticate('google', {
  successRedirect: '/LibaryFinder',
  failureRedirect: '/'
}));

function requireAuth(req, res, next) {
  if (req.isAuthenticated()) {
    // User is authenticated, allow access to the route
    return next();
  }
  
  // User is not authenticated, redirect to the login page
  res.redirect('/');
}

app.get("/", function (req, res) {
  res.render("home.ejs")
});

// Add the middleware to the routes that require authentication
app.get("/LibaryFinder", requireAuth, function (req, res) {
  res.render("dashboard.ejs",{name:req.user.displayName})
});

app.get("/register", requireAuth, function (req, res) {
  res.render("register")
});
// Busch
   // LSM
app.get("/busch_lsm", requireAuth, function(req,res){
    res.render("place",{name:" LSM",link1:"/busch_lsm/study_room1",link2:"/busch_lsm/study_room2"})
});
app.get("/busch_lsm/study_room1", requireAuth, function(req,res){
    res.render("lsm",{library:"LSM Study Room 1"})
});
app.get("/busch_lsm/study_room2", requireAuth, function(req,res){
  res.render("lsm",{library:"LSM Study Room 2"})
});
  //Student Center
app.get("/busch_studentcenter", requireAuth, function(req,res){
  res.render("place",{name:" Busch Student Center",link1:"/busch_studentcenter/study_room1",link2:"/busch_studentcenter/study_room2"})
});
app.get("/busch_studentcenter/study_room1", requireAuth, function(req,res){
  res.render("lsm",{library:"Busch Student Center Study Room 1"})
});
app.get("/busch_studentcenter/study_room2", requireAuth, function(req,res){
res.render("lsm",{library:"Busch Student Center Study Room 2"})
});

// Livi
  // James Dickson Library
app.get("/livingston_JamesDicksonLibrary", requireAuth, function(req,res){
  res.render("place",{name:" James Dickeson Library",link1:"/livingston_JamesDicksonLibrary/study_room1",link2:"/livingston_JamesDicksonLibrary/study_room2"})
});
app.get("/livingston_JamesDicksonLibrary/study_room1", requireAuth, function(req,res){
  res.render("lsm",{library:"James Dickson Library Study Room 1"})
});
app.get("/livingston_JamesDicksonLibrary/study_room2", requireAuth, function(req,res){
res.render("lsm",{library:"James Dickson Library Study Room 2"})
});

// Livi Student Center
app.get("/livingston_studentcenter", requireAuth, function(req,res){
  res.render("place",{name:" Livingston Student Center",link1:"/livingston_studentcenter/study_room1",link2:"/livingston_studentcenter/study_room2"})
});
app.get("/livingston_studentcenter/study_room1", requireAuth, function(req,res){
  res.render("lsm",{library:"Livingston Student Center Study Room 1"})
});
app.get("/livingston_studentcenter/study_room2", requireAuth, function(req,res){
res.render("lsm",{library:"Livingston Student Center Study Room 2"})
});

// College Ave
  //ArchibaldS.Alexander Library
app.get("/collegeAve_archibaldS.alexanderlibrary", requireAuth, function(req,res){
  res.render("place",{name:" ArchibaldS.Alexander Library",link1:"/collegeAve_archibaldS.alexanderlibrary/study_room1",link2:"/collegeAve_archibaldS.alexanderlibrary/study_room2"})
});
app.get("/collegeAve_archibaldS.alexanderlibrary/study_room1", requireAuth, function(req,res){
  res.render("lsm",{library:"ArchibaldS.Alexander Library Study Room 1"})
});
app.get("/collegeAve_archibaldS.alexanderlibrary/study_room2", requireAuth, function(req,res){
res.render("lsm",{library:"ArchibaldS.Alexander Library Study Room 2"})
});

// Collage Ave Student Center
app.get("/collegeAve_studentcenter", requireAuth, function(req,res){
  res.render("place",{name:" Collage Ave Student Center",link1:"/collegeAve_studentcenter/study_room1",link2:"/collegeAve_studentcenter/study_room2"})
});
app.get("/collegeAve_studentcenter/study_room1", requireAuth, function(req,res){
  res.render("lsm",{library:"Collage Ave Student Center Study Room 1"})
});
app.get("/collegeAve_studentcenter/study_room2", requireAuth, function(req,res){
res.render("lsm",{library:"Collage Ave Student Center Study Room 2"})
});
// Route for logging out the user

app.get("/logout",function(req,res){
    req.session = null;
    req.logout(function() {}); // add an empty callback function
    res.redirect("/");
});

app.listen(3000, function () {
  console.log("Server started on port 3000");
});
