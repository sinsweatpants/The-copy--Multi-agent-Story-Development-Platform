#!/usr/bin/env node

import { spawn } from 'child_process';
import { existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const rootDir = join(__dirname, '..');

// ANSI color codes
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  red: '\x1b[31m',
  cyan: '\x1b[36m'
};

const log = (msg, color = 'reset') => console.log(`${colors[color]}${msg}${colors.reset}`);
const logStep = (msg) => log(`\n${colors.bright}▶${colors.reset} ${msg}`, 'cyan');
const logSuccess = (msg) => log(`${colors.bright}✓${colors.reset} ${msg}`, 'green');
const logError = (msg) => log(`${colors.bright}✗${colors.reset} ${msg}`, 'red');
const logWarning = (msg) => log(`${colors.bright}⚠${colors.reset} ${msg}`, 'yellow');

// Check if dependencies are installed
function checkDependencies() {
  logStep('Checking dependencies...');

  const backendNodeModules = join(rootDir, 'jules-backend', 'node_modules');
  const frontendNodeModules = join(rootDir, 'jules-frontend', 'node_modules');

  if (!existsSync(backendNodeModules) || !existsSync(frontendNodeModules)) {
    logWarning('Dependencies not found. Installing...');
    return runCommand('npm', ['install'], rootDir);
  }

  logSuccess('Dependencies already installed');
  return Promise.resolve();
}

// Check if backend is built
function checkBackendBuild() {
  logStep('Checking backend build...');

  const backendDist = join(rootDir, 'jules-backend', 'dist');

  if (!existsSync(backendDist)) {
    logWarning('Backend not built. Building...');
    return runCommand('npm', ['run', 'build:backend'], rootDir);
  }

  logSuccess('Backend already built');
  return Promise.resolve();
}

// Check if frontend is built
function checkFrontendBuild() {
  logStep('Checking frontend build...');

  const frontendDist = join(rootDir, 'jules-frontend', 'dist');

  if (!existsSync(frontendDist)) {
    logWarning('Frontend not built. Building...');
    return runCommand('npm', ['run', 'build:frontend'], rootDir);
  }

  logSuccess('Frontend already built');
  return Promise.resolve();
}

// Run Prisma migrations
function runMigrations() {
  logStep('Running database migrations...');
  return runCommand('npm', ['run', 'prisma:migrate'], rootDir)
    .then(() => logSuccess('Migrations completed'))
    .catch((err) => {
      logWarning('Migrations skipped (database may not be configured)');
      return Promise.resolve();
    });
}

// Run a command and return a promise
function runCommand(command, args, cwd) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      cwd,
      stdio: 'inherit',
      shell: true
    });

    child.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Command failed with code ${code}`));
      } else {
        resolve();
      }
    });

    child.on('error', reject);
  });
}

// Start backend and frontend concurrently
function startServices() {
  logStep('Starting services...');

  log('\n' + '='.repeat(60), 'blue');
  log('  Jules Platform is starting...', 'bright');
  log('  Backend: http://localhost:8000', 'cyan');
  log('  Frontend: http://localhost:4173', 'cyan');
  log('  API Docs: http://localhost:8000/docs', 'cyan');
  log('='.repeat(60) + '\n', 'blue');

  const backend = spawn('npm', ['run', 'start:backend'], {
    cwd: rootDir,
    stdio: 'inherit',
    shell: true
  });

  // Wait a bit before starting frontend
  setTimeout(() => {
    const frontend = spawn('npm', ['run', 'start:frontend'], {
      cwd: rootDir,
      stdio: 'inherit',
      shell: true
    });

    frontend.on('error', (err) => {
      logError(`Frontend error: ${err.message}`);
      process.exit(1);
    });
  }, 2000);

  backend.on('error', (err) => {
    logError(`Backend error: ${err.message}`);
    process.exit(1);
  });

  // Handle graceful shutdown
  process.on('SIGINT', () => {
    log('\n\nShutting down gracefully...', 'yellow');
    backend.kill();
    process.exit(0);
  });
}

// Main execution
async function main() {
  try {
    log('\n' + '='.repeat(60), 'blue');
    log('  🚀 Jules Platform Startup Script', 'bright');
    log('='.repeat(60) + '\n', 'blue');

    await checkDependencies();
    await checkBackendBuild();
    await checkFrontendBuild();
    await runMigrations();

    startServices();
  } catch (error) {
    logError(`\nStartup failed: ${error.message}`);
    process.exit(1);
  }
}

main();
