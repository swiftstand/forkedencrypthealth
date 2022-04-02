import { Object, Property } from "fabric-contract-api";

@Object()
export class Asset {
    @Property()
    public docType?: string;

    @Property()
    public ID: string;

    @Property()
    public PatientID: String;

    @Property()
    public DoctorID: String;

    @Property()
    public Diagnosis: string;

    @Property()
    public TestsRequested: Array<string>;

}