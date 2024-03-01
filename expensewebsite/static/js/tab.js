const express = require('express');
const MongoClient = require('mongodb').MongoClient;
const app = express();

const mongoURI = "mongodb+srv://rithin:076ecHwHg60yETd9@cluster0.ctrleyy.mongodb.net/?retryWrites=true&w=majority"; // MongoDB connection URI
const dbName = 'TRADERZSPOT'; // Name of your MongoDB database

// Serve static files from the public directory
app.use(express.static('public'));

// Connect to MongoDB
MongoClient.connect(mongoURI, { useNewUrlParser: true, useUnifiedTopology: true }, (err, client) => {
    if (err) {
        console.error('Error connecting to MongoDB:', err);
        return;
    }

    console.log('Connected to MongoDB');

    const db = client.db(dbName);

    // Define routes
    app.get('/collection1', (req, res) => {
        db.collection('NSE:WIPRO-EQ').find({}).toArray((err, result) => {
            if (err) {
                console.error('Error retrieving data from collection1:', err);
                res.status(500).json({ error: 'Internal Server Error' });
                return;
            }
            res.json(result);
        });
    });

    app.get('/collection2', (req, res) => {
        db.collection('BANKNIFTY').find({}).toArray((err, result) => {
            if (err) {
                console.error('Error retrieving data from collection2:', err);
                res.status(500).json({ error: 'Internal Server Error' });
                return;
            }
            res.json(result);
        });
    });

    // Start the server
    const port = 3000;
    app.listen(port, () => {
        console.log(`Server running on http://localhost:${port}`);
    });
});