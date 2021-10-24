var accounts = null;

export function getAccounts() {
  return accounts;
}

export function setAccounts(accts) {
  accounts = accts;
}

export function isConnected() {
  return this.accounts !== null;
}
