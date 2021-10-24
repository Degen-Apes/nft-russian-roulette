import { ethers } from "ethers";
import {
  isDataURI,
  getMetadataFromDataURI,
  isIpfsUrl,
  getIPFSGatewayURL,
  isArweaveURL,
  getArweaveGatewayURL,
} from "./urls.js";
import erc721ABI from "./assets/erc721ABI.json";

let cache = {};

function computeCacheKey(chainID, contractAddress, tokenID) {
  return (
    chainID +
    "-" +
    contractAddress +
    "-" +
    ethers.BigNumber.from(tokenID).toString()
  );
}

export async function fetchERC721Metadata(
  provider,
  chainID,
  contractAddress,
  tokenID
) {
  const cacheKey = computeCacheKey(chainID, contractAddress, tokenID);
  if (cache[cacheKey]) {
    return cache[cacheKey];
  }

  const metadata = fetchJSONMetadataNoCache(provider, contractAddress, tokenID);
  cache[cacheKey] = metadata;

  return metadata;
}

async function fetchJSONMetadataNoCache(provider, contractAddress, tokenID) {
  const contract = new ethers.Contract(contractAddress, erc721ABI, provider);

  let uri = await contract.tokenURI(tokenID);
  if (uri.length === 0) {
    throw new Error("ERC721 URI of token is empty");
  }

  if (isDataURI(uri)) {
    return getMetadataFromDataURI(uri);
  }

  if (isIpfsUrl(uri)) {
    uri = getIPFSGatewayURL(uri);
  }
  if (isArweaveURL(uri)) {
    uri = getArweaveGatewayURL(uri);
  }

  const response = await window.fetch(uri);
  if (!response.ok) {
    throw new Error("failed to fetch ERC721 JSON metadata");
  }

  return await response.json();
}
