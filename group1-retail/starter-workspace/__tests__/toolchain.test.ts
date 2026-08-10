// Toolchain smoke test. It asserts nothing about PointHub — only that the workspace is
// wired up correctly, so `npm test` and `npm run typecheck` give you a green result before
// you start. Delete it once you have real tests, or leave it; it costs nothing.

describe('workspace toolchain', () => {
  it('runs on Node 20 or newer', () => {
    const major = Number(process.versions.node.split('.')[0]);
    expect(major).toBeGreaterThanOrEqual(20);
  });

  it('type-checks in strict mode', () => {
    // noUncheckedIndexedAccess is on, so this is string | undefined and must be handled.
    const tiers = ['SILVER', 'GOLD', 'PLATINUM'];
    const first = tiers[0];
    expect(first ?? 'NONE').toBe('SILVER');
  });

  it('does integer points math without floating point', () => {
    // 749 THB on a x2 campaign = 59_920 milli-points, which posts as 59 points.
    const milliPoints = 749 * (2000 / 25);
    expect(Number.isInteger(milliPoints)).toBe(true);
    expect(Math.floor(milliPoints / 1000)).toBe(59);
  });
});
