async function main() {
    const [deployer] = await ethers.getSigners();

    console.log("Deploying contracts with the account:", deployer.address);

    console.log("Account balance:", (await deployer.getBalance()).toString());

    const Gravestone = await ethers.getContractFactory("Gravestone");
    const gravestone = await Gravestone.deploy('Gravestone', 'GRST', 'https://api.nftrr.degen-apes.lol/gravestone/');
    console.log("Gravestone address:", gravestone.address);

    const RussianRoulette = await ethers.getContractFactory("Roulette");
    const roulette = await RussianRoulette.deploy(gravestone.address);
    console.log("Roulette address:", roulette.address);

    const grantTx = await gravestone.grantRole(gravestone.MINTER_ROLE(), roulette.address);
    await grantTx.wait();
    console.log('Minter role granted to Roulette');

    const emitTx = await roulette.killEvent("0x1230000000000000000000000000000000000000", "0x0000000000000000000000000000000000000001", 1, 1);
    await emitTx.wait();

    console.log('Gravestone minted and Event emitted');
    console.log('Token URI', await gravestone.tokenURI(0));
  }

  main()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error(error);
      process.exit(1);
    });
