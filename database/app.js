const express = require("express");
const fs = require("fs");

const app = express();
const port = 3030;

app.use(express.json({ type: "*/*" }));

function readJsonFile(candidates) {
  for (const file of candidates) {
    if (fs.existsSync(file)) {
      return JSON.parse(fs.readFileSync(file, "utf8"));
    }
  }
  throw new Error("Required JSON data file not found: " + candidates.join(", "));
}

const reviewsData = readJsonFile(["data/reviews.json", "reviews.json"]);
const dealershipsData = readJsonFile(["data/dealerships.json", "dealerships.json"]);

let reviews = reviewsData.reviews || reviewsData;
let dealerships = dealershipsData.dealerships || dealershipsData;

app.get("/", async (req, res) => {
  res.send("Dealership backend service is running");
});

app.get("/fetchReviews", async (req, res) => {
  res.json(reviews);
});

app.get("/fetchReviews/dealer/:id", async (req, res) => {
  const dealerId = Number(req.params.id);
  const documents = reviews.filter((review) => Number(review.dealership) === dealerId);
  res.json(documents);
});

app.get("/fetchDealers", async (req, res) => {
  res.json(dealerships);
});

app.get("/fetchDealers/:state", async (req, res) => {
  const state = req.params.state;
  if (state === "All") {
    res.json(dealerships);
    return;
  }
  const documents = dealerships.filter((dealer) => dealer.state === state);
  res.json(documents);
});

app.get("/fetchDealer/:id", async (req, res) => {
  const dealerId = Number(req.params.id);
  const documents = dealerships.filter((dealer) => Number(dealer.id) === dealerId);
  res.json(documents);
});

app.post("/insert_review", async (req, res) => {
  const data = req.body || {};
  const maxId = reviews.reduce((max, review) => Math.max(max, Number(review.id || 0)), 0);

  const review = {
    id: maxId + 1,
    name: data.name,
    dealership: Number(data.dealership),
    review: data.review,
    purchase: data.purchase,
    purchase_date: data.purchase_date,
    car_make: data.car_make,
    car_model: data.car_model,
    car_year: data.car_year,
    sentiment: data.sentiment || "neutral"
  };

  reviews.push(review);
  res.json(review);
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
