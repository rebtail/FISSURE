from fissure.comms.CertificateGenerator import CertificateGenerator

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
