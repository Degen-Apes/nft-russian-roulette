async function main() {
    const [deployer] = await ethers.getSigners();

    console.log("Deploying contracts with the account:", deployer.address);

    console.log("Account balance:", (await deployer.getBalance()).toString());

    const Gravestone = await ethers.getContractFactory("Gravestone");
    const gravestone = await Gravestone.deploy('Gravestone', 'GRST', 'https://nftrr.degen-apes.lol/gravestone/');

    console.log("Gravestone address:", gravestone.address);

    const RussianRoulette = await ethers.getContractFactory("Roulette");
    const roulette = await RussianRoulette.deploy(gravestone.address);

    console.log("Roulette address:", roulette.address);
  }

  main()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error(error);
      process.exit(1);
    });
