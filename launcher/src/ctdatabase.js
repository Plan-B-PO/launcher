var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/CTDatabase";

MongoClient.connect(url, function(err, db) {
  if (err) throw err;
  console.log("Database created!");
  db.createUser(
      {
          user  : "mongouser",
          pwd   : "user1234",
          roles : [
              {
                  role: "redWrite",
                  db: "CTDatabase"
              }
          ]
      }
  )
  db.close();
});