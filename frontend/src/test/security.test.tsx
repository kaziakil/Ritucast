import { describe, it, expect } from 'vitest'
import fs from 'node:fs'
import path from 'node:path'

describe('Frontend Security & Responsible Intelligence Verification (Phase 15)', () => {
  const srcDir = path.resolve(__dirname, '..')

  function getAllFiles(dir: string, ext: string[]): string[] {
    let results: string[] = []
    const list = fs.readdirSync(dir)
    for (const file of list) {
      const fullPath = path.join(dir, file)
      const stat = fs.statSync(fullPath)
      if (stat && stat.isDirectory()) {
        if (file !== 'test') {
          results = results.concat(getAllFiles(fullPath, ext))
        }
      } else if (ext.some(e => file.endsWith(e))) {
        results.push(fullPath)
      }
    }
    return results
  }

  it('verifies absence of dangerouslySetInnerHTML across all TSX components', () => {
    const files = getAllFiles(srcDir, ['.tsx', '.ts'])
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8')
      expect(content).not.toContain('dangerouslySetInnerHTML')
    }
  })

  it('verifies absence of eval and innerHTML direct assignment', () => {
    const files = getAllFiles(srcDir, ['.tsx', '.ts'])
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8')
      expect(content).not.toMatch(/\.innerHTML\s*=/)
      expect(content).not.toMatch(/\beval\s*\(/)
    }
  })

  it('verifies no private server secrets or cloud credentials in frontend source code', () => {
    const files = getAllFiles(srcDir, ['.tsx', '.ts', '.css'])
    const prohibitedPatterns = [
      /AIzaSy[0-9A-Za-z_-]{33}/, // Google API Key
      /AKIA[0-9A-Z]{16}/,        // AWS Access Key
      /ghp_[0-9a-zA-Z]{36}/,     // GitHub Personal Access Token
      /BEGIN (RSA|EC|PRIVATE) KEY/, // Private Key PEM
    ]

    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8')
      for (const pattern of prohibitedPatterns) {
        expect(content).not.toMatch(pattern)
      }
    }
  })

  it('verifies that apiClient does not silently suppress network errors with mock data', async () => {
    const apiClientPath = path.join(srcDir, 'services', 'apiClient.ts')
    const content = fs.readFileSync(apiClientPath, 'utf-8')

    // Confirm that apiClient throws ApiError on failed responses rather than returning synthetic mock data
    expect(content).toContain('throw new ApiError')
    expect(content).not.toContain('return MOCK_DATA')
  })
})
