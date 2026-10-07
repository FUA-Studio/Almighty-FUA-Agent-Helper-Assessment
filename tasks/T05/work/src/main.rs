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
    let mut map: HashMap<String, CategoryStat> = HashMap::new();

    for result in rdr.deserialize::<RawRecord>() {
        let record: RawRecord = result?;
        let entry = map.entry(record.category).or_insert(CategoryStat {
            category: String::new(),
            total: 0.0,
            count: 0,
            avg: 0.0,
        });
        entry.count += 1;
        entry.avg = entry.total / entry.count as f64;
        entry.total += record.value;
    }

    let stats: Vec<CategoryStat> = map.into_values().collect();
    serde_json::to_writer_pretty(std::io::stdout(), &stats)?;
    Ok(())
}
