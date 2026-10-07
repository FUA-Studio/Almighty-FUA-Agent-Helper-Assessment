use csv::ReaderBuilder;
use serde::Deserialize;
use serde::Serialize;
use std::collections::HashMap;
use std::fs::File;

#[derive(Debug, Deserialize)]
struct RawRecord {
    category: String,
    value: f64,
}

#[derive(Debug, Serialize)]
struct CategoryStat {
    category: String,
    total: f64,
    count: u64,
    avg: f64,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file = File::open("data.csv")?;
    let mut rdr = ReaderBuilder::new().has_headers(true).from_reader(file);
    let mut iter = rdr.deserialize::<RawRecord>().peekable();
    let mut map: HashMap<String, CategoryStat> = HashMap::new();

    while let Some(Ok(_record)) = iter.peek() {
        let rec = iter.next().unwrap()?;
        let cat = rec.category;
        let stat = map.entry(cat.clone()).or_insert(CategoryStat {
            category: String::new(),
            total: 0.0,
            count: 0,
            avg: 0.0,
        });
        stat.total += rec.value;
        stat.count += 1;
        stat.category = cat;
        stat.avg = stat.total / stat.count as f64;
    }

    let out = map.into_values().collect::<Vec<_>>();
    serde_json::to_writer_pretty(std::io::stdout(), &out)?;
    Ok(())
}
