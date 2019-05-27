db = db.getSiblingDB('whoscored'),
db.createUser({
    user: "whoscored",
    pwd: "whoscoredpassword",
    roles: ["readWrite"]
});
