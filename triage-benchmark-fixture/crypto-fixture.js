/**
 * Phase 5 golden-CBOM fixture — JavaScript (Node.js crypto module).
 * Exercises: AES-256-GCM (strong), SHA-256 (strong), RSA-3072 (strong), Ed25519 (strong),
 * MD5 (weak), DES (weak), RSA-1024 (weak), TLS via tls.createServer, PBKDF2 key material.
 */
'use strict';

const crypto = require('crypto');
const tls = require('tls');

// --- Strong algorithms ---

function strongSymmetric() {
    crypto.createCipheriv('aes-256-gcm', Buffer.alloc(32), Buffer.alloc(12));
}

function strongHash() {
    crypto.createHash('sha256');
}

function strongAsymmetric() {
    crypto.generateKeyPairSync('rsa', { modulusLength: 3072 });
    crypto.generateKeyPairSync('ed25519');
}

// --- Weak algorithms ---

function weakHash() {
    crypto.createHash('md5');
}

function weakSymmetric() {
    crypto.createCipheriv('des-ecb', Buffer.alloc(8), null);
    crypto.generateKeyPairSync('rsa', { modulusLength: 1024 });
}

// --- Protocol ---

function tlsProtocol() {
    tls.createServer({ minVersion: 'TLSv1.3' });
}

// --- Key derivation (related material) ---

function keyDerivation() {
    crypto.pbkdf2Sync('password', 'salt', 100000, 32, 'sha256');
    crypto.createHmac('sha256', 'key');
}
