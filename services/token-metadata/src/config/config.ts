import dotenv from 'dotenv'
import path from 'path'
import logger from '../utils/logger'

// Load .env file
dotenv.config({
  path: path.resolve(__dirname, '../../.env')
})

// Validate required environment variables
const requiredEnvVars = ['WALLET_PRIVATE_KEY']
const missingEnvVars = requiredEnvVars.filter(envVar => !process.env[envVar])

if (missingEnvVars.length > 0) {
  logger.error('Missing required environment variables', {
    missing: missingEnvVars
  })
  throw new Error(`Missing required environment variables: ${missingEnvVars.join(', ')}`)
}

export const config = {
  rpcEndpoint: process.env.RPC_ENDPOINT || 'https://api.mainnet-beta.solana.com',
  maxRetries: Number(process.env.MAX_RETRIES) || 3,
  confirmationTimeout: Number(process.env.CONFIRMATION_TIMEOUT) || 30000,
  walletPrivateKey: process.env.WALLET_PRIVATE_KEY as string,
  logLevel: process.env.LOG_LEVEL || 'debug'
}

logger.info('Configuration loaded', {
  rpcEndpoint: config.rpcEndpoint,
  maxRetries: config.maxRetries,
  confirmationTimeout: config.confirmationTimeout,
  logLevel: config.logLevel
})