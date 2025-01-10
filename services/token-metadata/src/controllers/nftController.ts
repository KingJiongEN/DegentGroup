import { Request, Response } from 'express'
import { NFTService } from '../services/nftService'
import { APIResponse, CreateNFTRequest, FetchByOwnerResponse } from '../types'
import logger from '../utils/logger'

export class NFTController {
  private nftService: NFTService

  constructor() {
    this.nftService = new NFTService()
  }

  async createNFT(req: Request, res: Response) {
    const requestId = Date.now().toString()
    logger.info('Received NFT creation request', {
      requestId,
      method: 'createNFT',
      body: req.body,
      ip: req.ip
    })

    try {
      const params = req.body as CreateNFTRequest

      // Log the validated parameters
      logger.debug('Validated request parameters', {
        requestId,
        params
      })

      const result = await this.nftService.createNFT(params)
      
      const response: APIResponse = {
        success: true,
        data: result,
        error: null
      }
      
      logger.info('NFT created successfully', {
        requestId,
        nftAddress: result.nft_address,
        signature: result.signature
      })

      res.json(response)
    } catch (error: any) {
      logger.error('NFT creation failed', {
        requestId,
        error: {
          message: error?.message,
          stack: error?.stack
        }
      })

      const response: APIResponse = {
        success: false,
        data: null,
        error: {
          code: 'CREATE_NFT_ERROR',
          message: error?.message || 'Unknown error occurred'
        }
      }
      
      res.status(500).json(response)
    }
  }

 
  async fetchByOwner(req: Request, res: Response) {
    const requestId = Date.now().toString()
    logger.info('Received fetch by owner request', {
      requestId,
      method: 'fetchByOwner',
      params: req.params,
      ip: req.ip
    })

    try {
      const { owner } = req.params
      const result = await this.nftService.fetchByOwner(owner)
      
      const response: APIResponse<FetchByOwnerResponse> = {
        success: true,
        data: { tokens: result },
        error: null
      }

      logger.info('Fetch by owner completed', {
        requestId,
        tokenCount: result.length
      })

      res.json(response)
    } catch (error: any) {
      logger.error('Fetch by owner failed', {
        requestId,
        error: {
          message: error?.message,
          stack: error?.stack
        }
      })

      const response: APIResponse = {
        success: false,
        data: null,
        error: {
          code: 'FETCH_ERROR',
          message: error?.message || 'Failed to fetch tokens'
        }
      }
      
      res.status(500).json(response)
    }
  }
}