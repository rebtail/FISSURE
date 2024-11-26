# from fissure import Dashboard, HiprFisr, ProtocolDiscovery, Server, TargetSignalIdentification
from fissure.comms.CertificateGenerator import CertificateGenerator

import fissure.Dashboard
import fissure.Server
import fissure.utils


def generate_certs():
    CG = CertificateGenerator()
    CG.create_server_certificates()
    CG.create_client_certificates()


def main():
    """
    """
    generate_certs()


if __name__ == "__main__":
    main()
