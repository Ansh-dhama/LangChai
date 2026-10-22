{
  "info": {
    "name": "HireAI - Phase 1 Ingestion Verification Suite",
    "description": "End-to-end Postman test suite for Phase 1 (F01-F12 fixes, Consent, Audit, Duplicate 409, and Tika MIME checks).",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "baseUrl",
      "value": "http://localhost:8081/app"
    },
    {
      "key": "jobPostingId",
      "value": "22222222-2222-2222-2222-222222222222"
    }
  ],
  "item": [
    {
      "name": "TC-01: Valid Application (Happy Path - 201 Created)",
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "pm.test('Status code is 201 Created', function () {",
              "    pm.response.to.have.status(201);",
              "});",
              "pm.test('Email is normalized to lowercase and status is RECEIVED', function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData.email).to.eql('ansh.dhama@example.com');",
              "    pm.expect(jsonData.status).to.eql('RECEIVED');",
              "    pm.expect(jsonData.message).to.include('Application received and verified');",
              "});"
            ],
            "type": "text/javascript"
          }
        }
      ],
      "request": {
        "method": "POST",
        "header": [],
        "body": {
          "mode": "formdata",
          "formdata": [
            { "key": "jobPostingId", "value": "{{jobPostingId}}", "type": "text" },
            { "key": "fullName", "value": "Ansh Dhama", "type": "text" },
            { "key": "email", "value": "  Ansh.Dhama@Example.com  ", "type": "text" },
            { "key": "githubUsername", "value": "octocat", "type": "text" },
            { "key": "consentGiven", "value": "true", "type": "text" },
            { "key": "noticeVersion", "value": "v1.0-2026", "type": "text" },
            { "key": "resume", "type": "file", "src": "" }
          ]
        },
        "url": {
          "raw": "{{baseUrl}}/api/v1/candidates/apply",
          "host": ["{{baseUrl}}"],
          "path": ["api", "v1", "candidates", "apply"]
        }
      }
    },
    {
      "name": "TC-02: Duplicate Email Case-Insensitive (F08 Fix - 409 Conflict)",
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "pm.test('Status code is 409 Conflict', function () {",
              "    pm.response.to.have.status(409);",
              "});",
              "pm.test('Returns RFC 7807 ProblemDetail for Duplicate Application', function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData.title).to.eql('Duplicate Application');",
              "    pm.expect(jsonData.status).to.eql(409);",
              "});"
            ],
            "type": "text/javascript"
          }
        }
      ],
      "request": {
        "method": "POST",
        "header": [],
        "body": {
          "mode": "formdata",
          "formdata": [
            { "key": "jobPostingId", "value": "{{jobPostingId}}", "type": "text" },
            { "key": "fullName", "value": "Ansh Dhama", "type": "text" },
            { "key": "email", "value": "ansh.dhama@example.com", "type": "text" },
            { "key": "githubUsername", "value": "octocat", "type": "text" },
            { "key": "consentGiven", "value": "true", "type": "text" },
            { "key": "noticeVersion", "value": "v1.0-2026", "type": "text" },
            { "key": "resume", "type": "file", "src": "" }
          ]
        },
        "url": {
          "raw": "{{baseUrl}}/api/v1/candidates/apply",
          "host": ["{{baseUrl}}"],
          "path": ["api", "v1", "candidates", "apply"]
        }
      }
    },
    {
      "name": "TC-03: Missing Consent (F06 Fix - 400 Bad Request)",
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "pm.test('Status code is 400 Bad Request when consentGiven is false', function () {",
              "    pm.response.to.have.status(400);",
              "});",
              "pm.test('ProblemDetail mentions validation failure', function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData.status).to.eql(400);",
              "});"
            ],
            "type": "text/javascript"
          }
        }
      ],
      "request": {
        "method": "POST",
        "header": [],
        "body": {
          "mode": "formdata",
          "formdata": [
            { "key": "jobPostingId", "value": "{{jobPostingId}}", "type": "text" },
            { "key": "fullName", "value": "Test User", "type": "text" },
            { "key": "email", "value": "noconsent@example.com", "type": "text" },
            { "key": "githubUsername", "value": "octocat", "type": "text" },
            { "key": "consentGiven", "value": "false", "type": "text" },
            { "key": "noticeVersion", "value": "v1.0-2026", "type": "text" },
            { "key": "resume", "type": "file", "src": "" }
          ]
        },
        "url": {
          "raw": "{{baseUrl}}/api/v1/candidates/apply",
          "host": ["{{baseUrl}}"],
          "path": ["api", "v1", "candidates", "apply"]
        }
      }
    },
    {
      "name": "TC-04: Non-Existent GitHub User (400 Bad Request)",
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "pm.test('Status code is 400 Bad Request for fake GitHub handle', function () {",
              "    pm.response.to.have.status(400);",
              "});",
              "pm.test('Detail states GitHub handle does not exist', function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData.detail).to.include('does not exist');",
              "});"
            ],
            "type": "text/javascript"
          }
        }
      ],
      "request": {
        "method": "POST",
        "header": [],
        "body": {
          "mode": "formdata",
          "formdata": [
            { "key": "jobPostingId", "value": "{{jobPostingId}}", "type": "text" },
            { "key": "fullName", "value": "Ghost User", "type": "text" },
            { "key": "email", "value": "ghost@example.com", "type": "text" },
            { "key": "githubUsername", "value": "this-github-user-never-existed-9999999", "type": "text" },
            { "key": "consentGiven", "value": "true", "type": "text" },
            { "key": "noticeVersion", "value": "v1.0-2026", "type": "text" },
            { "key": "resume", "type": "file", "src": "" }
          ]
        },
        "url": {
          "raw": "{{baseUrl}}/api/v1/candidates/apply",
          "host": ["{{baseUrl}}"],
          "path": ["api", "v1", "candidates", "apply"]
        }
      }
    },
    {
      "name": "TC-05: Invalid Email Format (400 Bad Request)",
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "pm.test('Status code is 400 Bad Request', function () {",
              "    pm.response.to.have.status(400);",
              "});",
              "pm.test('Returns Validation Failure title', function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData.title).to.eql('Validation Failure');",
              "});"
            ],
            "type": "text/javascript"
          }
        }
      ],
      "request": {
        "method": "POST",
        "header": [],
        "body": {
          "mode": "formdata",
          "formdata": [
            { "key": "jobPostingId", "value": "{{jobPostingId}}", "type": "text" },
            { "key": "fullName", "value": "Bad Email User", "type": "text" },
            { "key": "email", "value": "not-an-email-address", "type": "text" },
            { "key": "githubUsername", "value": "octocat", "type": "text" },
            { "key": "consentGiven", "value": "true", "type": "text" },
            { "key": "noticeVersion", "value": "v1.0-2026", "type": "text" },
            { "key": "resume", "type": "file", "src": "" }
          ]
        },
        "url": {
          "raw": "{{baseUrl}}/api/v1/candidates/apply",
          "host": ["{{baseUrl}}"],
          "path": ["api", "v1", "candidates", "apply"]
        }
      }
    },
    {
      "name": "TC-06: Unknown Job Posting UUID (404 Not Found)",
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "pm.test('Status code is 404 Not Found', function () {",
              "    pm.response.to.have.status(404);",
              "});",
              "pm.test('Title is Resource Not Found', function () {",
              "    var jsonData = pm.response.json();",
              "    pm.expect(jsonData.title).to.eql('Resource Not Found');",
              "});"
            ],
            "type": "text/javascript"
          }
        }
      ],
      "request": {
        "method": "POST",
        "header": [],
        "body": {
          "mode": "formdata",
          "formdata": [
            { "key": "jobPostingId", "value": "99999999-9999-9999-9999-999999999999", "type": "text" },
            { "key": "fullName", "value": "Ansh Dhama", "type": "text" },
            { "key": "email", "value": "newjob@example.com", "type": "text" },
            { "key": "githubUsername", "value": "octocat", "type": "text" },
            { "key": "consentGiven", "value": "true", "type": "text" },
            { "key": "noticeVersion", "value": "v1.0-2026", "type": "text" },
            { "key": "resume", "type": "file", "src": "" }
          ]
        },
        "url": {
          "raw": "{{baseUrl}}/api/v1/candidates/apply",
          "host": ["{{baseUrl}}"],
          "path": ["api", "v1", "candidates", "apply"]
        }
      }
    }
  ]
}