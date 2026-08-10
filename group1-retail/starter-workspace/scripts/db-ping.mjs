#!/usr/bin/env node
// Proves the workshop database is reachable, before you build anything against it.
//
//     npm run db:ping
//
// This is toolchain, not application code — it makes no assumption about your
// schema and creates nothing.
import pg from 'pg';

const url =
  process.env.DATABASE_URL ?? 'postgres://pointhub:pointhub@localhost:5432/pointhub';
const safe = url.replace(/:[^:@/]*@/, ':****@');
const client = new pg.Client({ connectionString: url, connectionTimeoutMillis: 5000 });

try {
  await client.connect();
  const { rows } = await client.query(
    "select current_database() as db, version() as v, now() at time zone 'UTC' as utc_now",
  );
  console.log(`  url      ${safe}`);
  console.log(`  database ${rows[0].db}`);
  console.log(`  server   ${rows[0].v.split(',')[0]}`);
  console.log(`  utc now  ${rows[0].utc_now.toISOString()}`);
  console.log('\ndatabase is up.');
} catch (err) {
  // pg leaves `message` empty for some connection failures — fall back to the code.
  const why = err.message?.trim() || err.code || String(err);
  console.error(`\ncannot reach the database at ${safe}`);
  console.error(`  ${why}\n`);
  console.error('Start it first, from this folder:');
  console.error('    docker compose up -d');
  console.error('`docker compose ps` should show "healthy" before you retry.');
  console.error('If Docker Desktop itself is not running, start that first.');
  process.exitCode = 1;
} finally {
  await client.end().catch(() => {});
}
