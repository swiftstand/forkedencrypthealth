import { Object, Property } from "fabric-contract-api";

@Object()
export class Asset {
    @Property()
    public docType?: string;

    @Property()
    public ID: string;

    @Property()
    public PatientID: string;

    @Property()
    public PolicyNumber: string;

    @Property()
    public RequestedAmt: number;

    @Property()
    public RequestStatus: string;

}
