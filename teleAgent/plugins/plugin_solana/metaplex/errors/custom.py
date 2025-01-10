import typing
from anchorpy.error import ProgramError


class InstructionUnpackError(ProgramError):
    def __init__(self) -> None:
        super().__init__(0, "")

    code = 0
    name = "InstructionUnpackError"
    msg = ""


class InstructionPackError(ProgramError):
    def __init__(self) -> None:
        super().__init__(1, "")

    code = 1
    name = "InstructionPackError"
    msg = ""


class NotRentExempt(ProgramError):
    def __init__(self) -> None:
        super().__init__(2, "Lamport balance below rent-exempt threshold")

    code = 2
    name = "NotRentExempt"
    msg = "Lamport balance below rent-exempt threshold"


class AlreadyInitialized(ProgramError):
    def __init__(self) -> None:
        super().__init__(3, "Already initialized")

    code = 3
    name = "AlreadyInitialized"
    msg = "Already initialized"


class Uninitialized(ProgramError):
    def __init__(self) -> None:
        super().__init__(4, "Uninitialized")

    code = 4
    name = "Uninitialized"
    msg = "Uninitialized"


class InvalidMetadataKey(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            5,
            " Metadata's key must match seed of ['metadata', program id, mint] provided",
        )

    code = 5
    name = "InvalidMetadataKey"
    msg = " Metadata's key must match seed of ['metadata', program id, mint] provided"


class InvalidEditionKey(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            6,
            "Edition's key must match seed of ['metadata', program id, name, 'edition'] provided",
        )

    code = 6
    name = "InvalidEditionKey"
    msg = "Edition's key must match seed of ['metadata', program id, name, 'edition'] provided"


class UpdateAuthorityIncorrect(ProgramError):
    def __init__(self) -> None:
        super().__init__(7, "Update Authority given does not match")

    code = 7
    name = "UpdateAuthorityIncorrect"
    msg = "Update Authority given does not match"


class UpdateAuthorityIsNotSigner(ProgramError):
    def __init__(self) -> None:
        super().__init__(8, "Update Authority needs to be signer to update metadata")

    code = 8
    name = "UpdateAuthorityIsNotSigner"
    msg = "Update Authority needs to be signer to update metadata"


class NotMintAuthority(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            9, "You must be the mint authority and signer on this transaction"
        )

    code = 9
    name = "NotMintAuthority"
    msg = "You must be the mint authority and signer on this transaction"


class InvalidMintAuthority(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            10, "Mint authority provided does not match the authority on the mint"
        )

    code = 10
    name = "InvalidMintAuthority"
    msg = "Mint authority provided does not match the authority on the mint"


class NameTooLong(ProgramError):
    def __init__(self) -> None:
        super().__init__(11, "Name too long")

    code = 11
    name = "NameTooLong"
    msg = "Name too long"


class SymbolTooLong(ProgramError):
    def __init__(self) -> None:
        super().__init__(12, "Symbol too long")

    code = 12
    name = "SymbolTooLong"
    msg = "Symbol too long"


class UriTooLong(ProgramError):
    def __init__(self) -> None:
        super().__init__(13, "URI too long")

    code = 13
    name = "UriTooLong"
    msg = "URI too long"


class UpdateAuthorityMustBeEqualToMetadataAuthorityAndSigner(ProgramError):
    def __init__(self) -> None:
        super().__init__(14, "")

    code = 14
    name = "UpdateAuthorityMustBeEqualToMetadataAuthorityAndSigner"
    msg = ""


class MintMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(15, "Mint given does not match mint on Metadata")

    code = 15
    name = "MintMismatch"
    msg = "Mint given does not match mint on Metadata"


class EditionsMustHaveExactlyOneToken(ProgramError):
    def __init__(self) -> None:
        super().__init__(16, "Editions must have exactly one token")

    code = 16
    name = "EditionsMustHaveExactlyOneToken"
    msg = "Editions must have exactly one token"


class MaxEditionsMintedAlready(ProgramError):
    def __init__(self) -> None:
        super().__init__(17, "")

    code = 17
    name = "MaxEditionsMintedAlready"
    msg = ""


class TokenMintToFailed(ProgramError):
    def __init__(self) -> None:
        super().__init__(18, "")

    code = 18
    name = "TokenMintToFailed"
    msg = ""


class MasterRecordMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(19, "")

    code = 19
    name = "MasterRecordMismatch"
    msg = ""


class DestinationMintMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(20, "")

    code = 20
    name = "DestinationMintMismatch"
    msg = ""


class EditionAlreadyMinted(ProgramError):
    def __init__(self) -> None:
        super().__init__(21, "")

    code = 21
    name = "EditionAlreadyMinted"
    msg = ""


class PrintingMintDecimalsShouldBeZero(ProgramError):
    def __init__(self) -> None:
        super().__init__(22, "")

    code = 22
    name = "PrintingMintDecimalsShouldBeZero"
    msg = ""


class OneTimePrintingAuthorizationMintDecimalsShouldBeZero(ProgramError):
    def __init__(self) -> None:
        super().__init__(23, "")

    code = 23
    name = "OneTimePrintingAuthorizationMintDecimalsShouldBeZero"
    msg = ""


class EditionMintDecimalsShouldBeZero(ProgramError):
    def __init__(self) -> None:
        super().__init__(24, "EditionMintDecimalsShouldBeZero")

    code = 24
    name = "EditionMintDecimalsShouldBeZero"
    msg = "EditionMintDecimalsShouldBeZero"


class TokenBurnFailed(ProgramError):
    def __init__(self) -> None:
        super().__init__(25, "")

    code = 25
    name = "TokenBurnFailed"
    msg = ""


class TokenAccountOneTimeAuthMintMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(26, "")

    code = 26
    name = "TokenAccountOneTimeAuthMintMismatch"
    msg = ""


class DerivedKeyInvalid(ProgramError):
    def __init__(self) -> None:
        super().__init__(27, "Derived key invalid")

    code = 27
    name = "DerivedKeyInvalid"
    msg = "Derived key invalid"


class PrintingMintMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            28, "The Printing mint does not match that on the master edition!"
        )

    code = 28
    name = "PrintingMintMismatch"
    msg = "The Printing mint does not match that on the master edition!"


class OneTimePrintingAuthMintMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            29,
            "The One Time Printing Auth mint does not match that on the master edition!",
        )

    code = 29
    name = "OneTimePrintingAuthMintMismatch"
    msg = "The One Time Printing Auth mint does not match that on the master edition!"


class TokenAccountMintMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            30, "The mint of the token account does not match the Printing mint!"
        )

    code = 30
    name = "TokenAccountMintMismatch"
    msg = "The mint of the token account does not match the Printing mint!"


class TokenAccountMintMismatchV2(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            31, "The mint of the token account does not match the master metadata mint!"
        )

    code = 31
    name = "TokenAccountMintMismatchV2"
    msg = "The mint of the token account does not match the master metadata mint!"


class NotEnoughTokens(ProgramError):
    def __init__(self) -> None:
        super().__init__(32, "Not enough tokens to mint a limited edition")

    code = 32
    name = "NotEnoughTokens"
    msg = "Not enough tokens to mint a limited edition"


class PrintingMintAuthorizationAccountMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(33, "")

    code = 33
    name = "PrintingMintAuthorizationAccountMismatch"
    msg = ""


class AuthorizationTokenAccountOwnerMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(34, "")

    code = 34
    name = "AuthorizationTokenAccountOwnerMismatch"
    msg = ""


class Disabled(ProgramError):
    def __init__(self) -> None:
        super().__init__(35, "")

    code = 35
    name = "Disabled"
    msg = ""


class CreatorsTooLong(ProgramError):
    def __init__(self) -> None:
        super().__init__(36, "Creators list too long")

    code = 36
    name = "CreatorsTooLong"
    msg = "Creators list too long"


class CreatorsMustBeAtleastOne(ProgramError):
    def __init__(self) -> None:
        super().__init__(37, "Creators must be at least one if set")

    code = 37
    name = "CreatorsMustBeAtleastOne"
    msg = "Creators must be at least one if set"


class MustBeOneOfCreators(ProgramError):
    def __init__(self) -> None:
        super().__init__(38, "")

    code = 38
    name = "MustBeOneOfCreators"
    msg = ""


class NoCreatorsPresentOnMetadata(ProgramError):
    def __init__(self) -> None:
        super().__init__(39, "This metadata does not have creators")

    code = 39
    name = "NoCreatorsPresentOnMetadata"
    msg = "This metadata does not have creators"


class CreatorNotFound(ProgramError):
    def __init__(self) -> None:
        super().__init__(40, "This creator address was not found")

    code = 40
    name = "CreatorNotFound"
    msg = "This creator address was not found"


class InvalidBasisPoints(ProgramError):
    def __init__(self) -> None:
        super().__init__(41, "Basis points cannot be more than 10000")

    code = 41
    name = "InvalidBasisPoints"
    msg = "Basis points cannot be more than 10000"


class PrimarySaleCanOnlyBeFlippedToTrue(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            42, "Primary sale can only be flipped to true and is immutable"
        )

    code = 42
    name = "PrimarySaleCanOnlyBeFlippedToTrue"
    msg = "Primary sale can only be flipped to true and is immutable"


class OwnerMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(43, "Owner does not match that on the account given")

    code = 43
    name = "OwnerMismatch"
    msg = "Owner does not match that on the account given"


class NoBalanceInAccountForAuthorization(ProgramError):
    def __init__(self) -> None:
        super().__init__(44, "This account has no tokens to be used for authorization")

    code = 44
    name = "NoBalanceInAccountForAuthorization"
    msg = "This account has no tokens to be used for authorization"


class ShareTotalMustBe100(ProgramError):
    def __init__(self) -> None:
        super().__init__(45, "Share total must equal 100 for creator array")

    code = 45
    name = "ShareTotalMustBe100"
    msg = "Share total must equal 100 for creator array"


class ReservationExists(ProgramError):
    def __init__(self) -> None:
        super().__init__(46, "")

    code = 46
    name = "ReservationExists"
    msg = ""


class ReservationDoesNotExist(ProgramError):
    def __init__(self) -> None:
        super().__init__(47, "")

    code = 47
    name = "ReservationDoesNotExist"
    msg = ""


class ReservationNotSet(ProgramError):
    def __init__(self) -> None:
        super().__init__(48, "")

    code = 48
    name = "ReservationNotSet"
    msg = ""


class ReservationAlreadyMade(ProgramError):
    def __init__(self) -> None:
        super().__init__(49, "")

    code = 49
    name = "ReservationAlreadyMade"
    msg = ""


class BeyondMaxAddressSize(ProgramError):
    def __init__(self) -> None:
        super().__init__(50, "")

    code = 50
    name = "BeyondMaxAddressSize"
    msg = ""


class NumericalOverflowError(ProgramError):
    def __init__(self) -> None:
        super().__init__(51, "NumericalOverflowError")

    code = 51
    name = "NumericalOverflowError"
    msg = "NumericalOverflowError"


class ReservationBreachesMaximumSupply(ProgramError):
    def __init__(self) -> None:
        super().__init__(52, "")

    code = 52
    name = "ReservationBreachesMaximumSupply"
    msg = ""


class AddressNotInReservation(ProgramError):
    def __init__(self) -> None:
        super().__init__(53, "")

    code = 53
    name = "AddressNotInReservation"
    msg = ""


class CannotVerifyAnotherCreator(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            54, "You cannot unilaterally verify another creator, they must sign"
        )

    code = 54
    name = "CannotVerifyAnotherCreator"
    msg = "You cannot unilaterally verify another creator, they must sign"


class CannotUnverifyAnotherCreator(ProgramError):
    def __init__(self) -> None:
        super().__init__(55, "You cannot unilaterally unverify another creator")

    code = 55
    name = "CannotUnverifyAnotherCreator"
    msg = "You cannot unilaterally unverify another creator"


class SpotMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(56, "")

    code = 56
    name = "SpotMismatch"
    msg = ""


class IncorrectOwner(ProgramError):
    def __init__(self) -> None:
        super().__init__(57, "Incorrect account owner")

    code = 57
    name = "IncorrectOwner"
    msg = "Incorrect account owner"


class PrintingWouldBreachMaximumSupply(ProgramError):
    def __init__(self) -> None:
        super().__init__(58, "")

    code = 58
    name = "PrintingWouldBreachMaximumSupply"
    msg = ""


class DataIsImmutable(ProgramError):
    def __init__(self) -> None:
        super().__init__(59, "Data is immutable")

    code = 59
    name = "DataIsImmutable"
    msg = "Data is immutable"


class DuplicateCreatorAddress(ProgramError):
    def __init__(self) -> None:
        super().__init__(60, "No duplicate creator addresses")

    code = 60
    name = "DuplicateCreatorAddress"
    msg = "No duplicate creator addresses"


class ReservationSpotsRemainingShouldMatchTotalSpotsAtStart(ProgramError):
    def __init__(self) -> None:
        super().__init__(61, "")

    code = 61
    name = "ReservationSpotsRemainingShouldMatchTotalSpotsAtStart"
    msg = ""


class InvalidTokenProgram(ProgramError):
    def __init__(self) -> None:
        super().__init__(62, "Invalid token program")

    code = 62
    name = "InvalidTokenProgram"
    msg = "Invalid token program"


class DataTypeMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(63, "Data type mismatch")

    code = 63
    name = "DataTypeMismatch"
    msg = "Data type mismatch"


class BeyondAlottedAddressSize(ProgramError):
    def __init__(self) -> None:
        super().__init__(64, "")

    code = 64
    name = "BeyondAlottedAddressSize"
    msg = ""


class ReservationNotComplete(ProgramError):
    def __init__(self) -> None:
        super().__init__(65, "")

    code = 65
    name = "ReservationNotComplete"
    msg = ""


class TriedToReplaceAnExistingReservation(ProgramError):
    def __init__(self) -> None:
        super().__init__(66, "")

    code = 66
    name = "TriedToReplaceAnExistingReservation"
    msg = ""


class InvalidOperation(ProgramError):
    def __init__(self) -> None:
        super().__init__(67, "Invalid operation")

    code = 67
    name = "InvalidOperation"
    msg = "Invalid operation"


class InvalidOwner(ProgramError):
    def __init__(self) -> None:
        super().__init__(68, "Invalid Owner")

    code = 68
    name = "InvalidOwner"
    msg = "Invalid Owner"


class PrintingMintSupplyMustBeZeroForConversion(ProgramError):
    def __init__(self) -> None:
        super().__init__(69, "Printing mint supply must be zero for conversion")

    code = 69
    name = "PrintingMintSupplyMustBeZeroForConversion"
    msg = "Printing mint supply must be zero for conversion"


class OneTimeAuthMintSupplyMustBeZeroForConversion(ProgramError):
    def __init__(self) -> None:
        super().__init__(70, "One Time Auth mint supply must be zero for conversion")

    code = 70
    name = "OneTimeAuthMintSupplyMustBeZeroForConversion"
    msg = "One Time Auth mint supply must be zero for conversion"


class InvalidEditionIndex(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            71, "You tried to insert one edition too many into an edition mark pda"
        )

    code = 71
    name = "InvalidEditionIndex"
    msg = "You tried to insert one edition too many into an edition mark pda"


class ReservationArrayShouldBeSizeOne(ProgramError):
    def __init__(self) -> None:
        super().__init__(72, "")

    code = 72
    name = "ReservationArrayShouldBeSizeOne"
    msg = ""


class IsMutableCanOnlyBeFlippedToFalse(ProgramError):
    def __init__(self) -> None:
        super().__init__(73, "Is Mutable can only be flipped to false")

    code = 73
    name = "IsMutableCanOnlyBeFlippedToFalse"
    msg = "Is Mutable can only be flipped to false"


class CollectionCannotBeVerifiedInThisInstruction(ProgramError):
    def __init__(self) -> None:
        super().__init__(74, "Collection cannot be verified in this instruction")

    code = 74
    name = "CollectionCannotBeVerifiedInThisInstruction"
    msg = "Collection cannot be verified in this instruction"


class Removed(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            75,
            "This instruction was deprecated in a previous release and is now removed",
        )

    code = 75
    name = "Removed"
    msg = "This instruction was deprecated in a previous release and is now removed"


class MustBeBurned(ProgramError):
    def __init__(self) -> None:
        super().__init__(76, "")

    code = 76
    name = "MustBeBurned"
    msg = ""


class InvalidUseMethod(ProgramError):
    def __init__(self) -> None:
        super().__init__(77, "This use method is invalid")

    code = 77
    name = "InvalidUseMethod"
    msg = "This use method is invalid"


class CannotChangeUseMethodAfterFirstUse(ProgramError):
    def __init__(self) -> None:
        super().__init__(78, "Cannot Change Use Method after the first use")

    code = 78
    name = "CannotChangeUseMethodAfterFirstUse"
    msg = "Cannot Change Use Method after the first use"


class CannotChangeUsesAfterFirstUse(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            79, "Cannot Change Remaining or Available uses after the first use"
        )

    code = 79
    name = "CannotChangeUsesAfterFirstUse"
    msg = "Cannot Change Remaining or Available uses after the first use"


class CollectionNotFound(ProgramError):
    def __init__(self) -> None:
        super().__init__(80, "Collection Not Found on Metadata")

    code = 80
    name = "CollectionNotFound"
    msg = "Collection Not Found on Metadata"


class InvalidCollectionUpdateAuthority(ProgramError):
    def __init__(self) -> None:
        super().__init__(81, "Collection Update Authority is invalid")

    code = 81
    name = "InvalidCollectionUpdateAuthority"
    msg = "Collection Update Authority is invalid"


class CollectionMustBeAUniqueMasterEdition(ProgramError):
    def __init__(self) -> None:
        super().__init__(82, "Collection Must Be a Unique Master Edition v2")

    code = 82
    name = "CollectionMustBeAUniqueMasterEdition"
    msg = "Collection Must Be a Unique Master Edition v2"


class UseAuthorityRecordAlreadyExists(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            83,
            "The Use Authority Record Already Exists, to modify it Revoke, then Approve",
        )

    code = 83
    name = "UseAuthorityRecordAlreadyExists"
    msg = "The Use Authority Record Already Exists, to modify it Revoke, then Approve"


class UseAuthorityRecordAlreadyRevoked(ProgramError):
    def __init__(self) -> None:
        super().__init__(84, "The Use Authority Record is empty or already revoked")

    code = 84
    name = "UseAuthorityRecordAlreadyRevoked"
    msg = "The Use Authority Record is empty or already revoked"


class Unusable(ProgramError):
    def __init__(self) -> None:
        super().__init__(85, "This token has no uses")

    code = 85
    name = "Unusable"
    msg = "This token has no uses"


class NotEnoughUses(ProgramError):
    def __init__(self) -> None:
        super().__init__(86, "There are not enough Uses left on this token.")

    code = 86
    name = "NotEnoughUses"
    msg = "There are not enough Uses left on this token."


class CollectionAuthorityRecordAlreadyExists(ProgramError):
    def __init__(self) -> None:
        super().__init__(87, "This Collection Authority Record Already Exists.")

    code = 87
    name = "CollectionAuthorityRecordAlreadyExists"
    msg = "This Collection Authority Record Already Exists."


class CollectionAuthorityDoesNotExist(ProgramError):
    def __init__(self) -> None:
        super().__init__(88, "This Collection Authority Record Does Not Exist.")

    code = 88
    name = "CollectionAuthorityDoesNotExist"
    msg = "This Collection Authority Record Does Not Exist."


class InvalidUseAuthorityRecord(ProgramError):
    def __init__(self) -> None:
        super().__init__(89, "This Use Authority Record is invalid.")

    code = 89
    name = "InvalidUseAuthorityRecord"
    msg = "This Use Authority Record is invalid."


class InvalidCollectionAuthorityRecord(ProgramError):
    def __init__(self) -> None:
        super().__init__(90, "")

    code = 90
    name = "InvalidCollectionAuthorityRecord"
    msg = ""


class InvalidFreezeAuthority(ProgramError):
    def __init__(self) -> None:
        super().__init__(91, "Metadata does not match the freeze authority on the mint")

    code = 91
    name = "InvalidFreezeAuthority"
    msg = "Metadata does not match the freeze authority on the mint"


class InvalidDelegate(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            92, "All tokens in this account have not been delegated to this user."
        )

    code = 92
    name = "InvalidDelegate"
    msg = "All tokens in this account have not been delegated to this user."


class CannotAdjustVerifiedCreator(ProgramError):
    def __init__(self) -> None:
        super().__init__(93, "")

    code = 93
    name = "CannotAdjustVerifiedCreator"
    msg = ""


class CannotRemoveVerifiedCreator(ProgramError):
    def __init__(self) -> None:
        super().__init__(94, "Verified creators cannot be removed.")

    code = 94
    name = "CannotRemoveVerifiedCreator"
    msg = "Verified creators cannot be removed."


class CannotWipeVerifiedCreators(ProgramError):
    def __init__(self) -> None:
        super().__init__(95, "")

    code = 95
    name = "CannotWipeVerifiedCreators"
    msg = ""


class NotAllowedToChangeSellerFeeBasisPoints(ProgramError):
    def __init__(self) -> None:
        super().__init__(96, "")

    code = 96
    name = "NotAllowedToChangeSellerFeeBasisPoints"
    msg = ""


class EditionOverrideCannotBeZero(ProgramError):
    def __init__(self) -> None:
        super().__init__(97, "Edition override cannot be zero")

    code = 97
    name = "EditionOverrideCannotBeZero"
    msg = "Edition override cannot be zero"


class InvalidUser(ProgramError):
    def __init__(self) -> None:
        super().__init__(98, "Invalid User")

    code = 98
    name = "InvalidUser"
    msg = "Invalid User"


class RevokeCollectionAuthoritySignerIncorrect(ProgramError):
    def __init__(self) -> None:
        super().__init__(99, "Revoke Collection Authority signer is incorrect")

    code = 99
    name = "RevokeCollectionAuthoritySignerIncorrect"
    msg = "Revoke Collection Authority signer is incorrect"


class TokenCloseFailed(ProgramError):
    def __init__(self) -> None:
        super().__init__(100, "")

    code = 100
    name = "TokenCloseFailed"
    msg = ""


class UnsizedCollection(ProgramError):
    def __init__(self) -> None:
        super().__init__(101, "Can't use this function on unsized collection")

    code = 101
    name = "UnsizedCollection"
    msg = "Can't use this function on unsized collection"


class SizedCollection(ProgramError):
    def __init__(self) -> None:
        super().__init__(102, "Can't use this function on a sized collection")

    code = 102
    name = "SizedCollection"
    msg = "Can't use this function on a sized collection"


class MissingCollectionMetadata(ProgramError):
    def __init__(self) -> None:
        super().__init__(103, "Missing collection metadata account")

    code = 103
    name = "MissingCollectionMetadata"
    msg = "Missing collection metadata account"


class NotAMemberOfCollection(ProgramError):
    def __init__(self) -> None:
        super().__init__(104, "This NFT is not a member of the specified collection.")

    code = 104
    name = "NotAMemberOfCollection"
    msg = "This NFT is not a member of the specified collection."


class NotVerifiedMemberOfCollection(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            105, "This NFT is not a verified member of the specified collection."
        )

    code = 105
    name = "NotVerifiedMemberOfCollection"
    msg = "This NFT is not a verified member of the specified collection."


class NotACollectionParent(ProgramError):
    def __init__(self) -> None:
        super().__init__(106, "This NFT is not a collection parent NFT.")

    code = 106
    name = "NotACollectionParent"
    msg = "This NFT is not a collection parent NFT."


class CouldNotDetermineTokenStandard(ProgramError):
    def __init__(self) -> None:
        super().__init__(107, "Could not determine a TokenStandard type.")

    code = 107
    name = "CouldNotDetermineTokenStandard"
    msg = "Could not determine a TokenStandard type."


class MissingEditionAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(108, "This mint account has an edition but none was provided.")

    code = 108
    name = "MissingEditionAccount"
    msg = "This mint account has an edition but none was provided."


class NotAMasterEdition(ProgramError):
    def __init__(self) -> None:
        super().__init__(109, "This edition is not a Master Edition")

    code = 109
    name = "NotAMasterEdition"
    msg = "This edition is not a Master Edition"


class MasterEditionHasPrints(ProgramError):
    def __init__(self) -> None:
        super().__init__(110, "This Master Edition has existing prints")

    code = 110
    name = "MasterEditionHasPrints"
    msg = "This Master Edition has existing prints"


class BorshDeserializationError(ProgramError):
    def __init__(self) -> None:
        super().__init__(111, "")

    code = 111
    name = "BorshDeserializationError"
    msg = ""


class CannotUpdateVerifiedCollection(ProgramError):
    def __init__(self) -> None:
        super().__init__(112, "Cannot update a verified collection in this command")

    code = 112
    name = "CannotUpdateVerifiedCollection"
    msg = "Cannot update a verified collection in this command"


class CollectionMasterEditionAccountInvalid(ProgramError):
    def __init__(self) -> None:
        super().__init__(113, "Edition account doesnt match collection ")

    code = 113
    name = "CollectionMasterEditionAccountInvalid"
    msg = "Edition account doesnt match collection "


class AlreadyVerified(ProgramError):
    def __init__(self) -> None:
        super().__init__(114, "Item is already verified.")

    code = 114
    name = "AlreadyVerified"
    msg = "Item is already verified."


class AlreadyUnverified(ProgramError):
    def __init__(self) -> None:
        super().__init__(115, "")

    code = 115
    name = "AlreadyUnverified"
    msg = ""


class NotAPrintEdition(ProgramError):
    def __init__(self) -> None:
        super().__init__(116, "This edition is not a Print Edition")

    code = 116
    name = "NotAPrintEdition"
    msg = "This edition is not a Print Edition"


class InvalidMasterEdition(ProgramError):
    def __init__(self) -> None:
        super().__init__(117, "Invalid Master Edition")

    code = 117
    name = "InvalidMasterEdition"
    msg = "Invalid Master Edition"


class InvalidPrintEdition(ProgramError):
    def __init__(self) -> None:
        super().__init__(118, "Invalid Print Edition")

    code = 118
    name = "InvalidPrintEdition"
    msg = "Invalid Print Edition"


class InvalidEditionMarker(ProgramError):
    def __init__(self) -> None:
        super().__init__(119, "Invalid Edition Marker")

    code = 119
    name = "InvalidEditionMarker"
    msg = "Invalid Edition Marker"


class ReservationListDeprecated(ProgramError):
    def __init__(self) -> None:
        super().__init__(120, "Reservation List is Deprecated")

    code = 120
    name = "ReservationListDeprecated"
    msg = "Reservation List is Deprecated"


class PrintEditionDoesNotMatchMasterEdition(ProgramError):
    def __init__(self) -> None:
        super().__init__(121, "Print Edition does not match Master Edition")

    code = 121
    name = "PrintEditionDoesNotMatchMasterEdition"
    msg = "Print Edition does not match Master Edition"


class EditionNumberGreaterThanMaxSupply(ProgramError):
    def __init__(self) -> None:
        super().__init__(122, "Edition Number greater than max supply")

    code = 122
    name = "EditionNumberGreaterThanMaxSupply"
    msg = "Edition Number greater than max supply"


class MustUnverify(ProgramError):
    def __init__(self) -> None:
        super().__init__(123, "Must unverify before migrating collections.")

    code = 123
    name = "MustUnverify"
    msg = "Must unverify before migrating collections."


class InvalidEscrowBumpSeed(ProgramError):
    def __init__(self) -> None:
        super().__init__(124, "Invalid Escrow Account Bump Seed")

    code = 124
    name = "InvalidEscrowBumpSeed"
    msg = "Invalid Escrow Account Bump Seed"


class MustBeEscrowAuthority(ProgramError):
    def __init__(self) -> None:
        super().__init__(125, "Must Escrow Authority")

    code = 125
    name = "MustBeEscrowAuthority"
    msg = "Must Escrow Authority"


class InvalidSystemProgram(ProgramError):
    def __init__(self) -> None:
        super().__init__(126, "Invalid System Program")

    code = 126
    name = "InvalidSystemProgram"
    msg = "Invalid System Program"


class MustBeNonFungible(ProgramError):
    def __init__(self) -> None:
        super().__init__(127, "Must be a Non Fungible Token")

    code = 127
    name = "MustBeNonFungible"
    msg = "Must be a Non Fungible Token"


class InsufficientTokens(ProgramError):
    def __init__(self) -> None:
        super().__init__(128, "Insufficient tokens for transfer")

    code = 128
    name = "InsufficientTokens"
    msg = "Insufficient tokens for transfer"


class BorshSerializationError(ProgramError):
    def __init__(self) -> None:
        super().__init__(129, "Borsh Serialization Error")

    code = 129
    name = "BorshSerializationError"
    msg = "Borsh Serialization Error"


class NoFreezeAuthoritySet(ProgramError):
    def __init__(self) -> None:
        super().__init__(130, "Cannot create NFT with no Freeze Authority.")

    code = 130
    name = "NoFreezeAuthoritySet"
    msg = "Cannot create NFT with no Freeze Authority."


class InvalidCollectionSizeChange(ProgramError):
    def __init__(self) -> None:
        super().__init__(131, "Invalid collection size change")

    code = 131
    name = "InvalidCollectionSizeChange"
    msg = "Invalid collection size change"


class InvalidBubblegumSigner(ProgramError):
    def __init__(self) -> None:
        super().__init__(132, "Invalid bubblegum signer")

    code = 132
    name = "InvalidBubblegumSigner"
    msg = "Invalid bubblegum signer"


class EscrowParentHasDelegate(ProgramError):
    def __init__(self) -> None:
        super().__init__(133, "Escrow parent cannot have a delegate")

    code = 133
    name = "EscrowParentHasDelegate"
    msg = "Escrow parent cannot have a delegate"


class MintIsNotSigner(ProgramError):
    def __init__(self) -> None:
        super().__init__(134, "Mint needs to be signer to initialize the account")

    code = 134
    name = "MintIsNotSigner"
    msg = "Mint needs to be signer to initialize the account"


class InvalidTokenStandard(ProgramError):
    def __init__(self) -> None:
        super().__init__(135, "Invalid token standard")

    code = 135
    name = "InvalidTokenStandard"
    msg = "Invalid token standard"


class InvalidMintForTokenStandard(ProgramError):
    def __init__(self) -> None:
        super().__init__(136, "Invalid mint account for specified token standard")

    code = 136
    name = "InvalidMintForTokenStandard"
    msg = "Invalid mint account for specified token standard"


class InvalidAuthorizationRules(ProgramError):
    def __init__(self) -> None:
        super().__init__(137, "Invalid authorization rules account")

    code = 137
    name = "InvalidAuthorizationRules"
    msg = "Invalid authorization rules account"


class MissingAuthorizationRules(ProgramError):
    def __init__(self) -> None:
        super().__init__(138, "Missing authorization rules account")

    code = 138
    name = "MissingAuthorizationRules"
    msg = "Missing authorization rules account"


class MissingProgrammableConfig(ProgramError):
    def __init__(self) -> None:
        super().__init__(139, "Missing programmable configuration")

    code = 139
    name = "MissingProgrammableConfig"
    msg = "Missing programmable configuration"


class InvalidProgrammableConfig(ProgramError):
    def __init__(self) -> None:
        super().__init__(140, "Invalid programmable configuration")

    code = 140
    name = "InvalidProgrammableConfig"
    msg = "Invalid programmable configuration"


class DelegateAlreadyExists(ProgramError):
    def __init__(self) -> None:
        super().__init__(141, "Delegate already exists")

    code = 141
    name = "DelegateAlreadyExists"
    msg = "Delegate already exists"


class DelegateNotFound(ProgramError):
    def __init__(self) -> None:
        super().__init__(142, "Delegate not found")

    code = 142
    name = "DelegateNotFound"
    msg = "Delegate not found"


class MissingAccountInBuilder(ProgramError):
    def __init__(self) -> None:
        super().__init__(143, "Required account not set in instruction builder")

    code = 143
    name = "MissingAccountInBuilder"
    msg = "Required account not set in instruction builder"


class MissingArgumentInBuilder(ProgramError):
    def __init__(self) -> None:
        super().__init__(144, "Required argument not set in instruction builder")

    code = 144
    name = "MissingArgumentInBuilder"
    msg = "Required argument not set in instruction builder"


class FeatureNotSupported(ProgramError):
    def __init__(self) -> None:
        super().__init__(145, "Feature not supported currently")

    code = 145
    name = "FeatureNotSupported"
    msg = "Feature not supported currently"


class InvalidSystemWallet(ProgramError):
    def __init__(self) -> None:
        super().__init__(146, "Invalid system wallet")

    code = 146
    name = "InvalidSystemWallet"
    msg = "Invalid system wallet"


class OnlySaleDelegateCanTransfer(ProgramError):
    def __init__(self) -> None:
        super().__init__(147, "Only the sale delegate can transfer while its set")

    code = 147
    name = "OnlySaleDelegateCanTransfer"
    msg = "Only the sale delegate can transfer while its set"


class MissingTokenAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(148, "Missing token account")

    code = 148
    name = "MissingTokenAccount"
    msg = "Missing token account"


class MissingSplTokenProgram(ProgramError):
    def __init__(self) -> None:
        super().__init__(149, "Missing SPL token program")

    code = 149
    name = "MissingSplTokenProgram"
    msg = "Missing SPL token program"


class MissingAuthorizationRulesProgram(ProgramError):
    def __init__(self) -> None:
        super().__init__(150, "Missing authorization rules program")

    code = 150
    name = "MissingAuthorizationRulesProgram"
    msg = "Missing authorization rules program"


class InvalidDelegateRoleForTransfer(ProgramError):
    def __init__(self) -> None:
        super().__init__(151, "Invalid delegate role for transfer")

    code = 151
    name = "InvalidDelegateRoleForTransfer"
    msg = "Invalid delegate role for transfer"


class InvalidTransferAuthority(ProgramError):
    def __init__(self) -> None:
        super().__init__(152, "Invalid transfer authority")

    code = 152
    name = "InvalidTransferAuthority"
    msg = "Invalid transfer authority"


class InstructionNotSupported(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            153, "Instruction not supported for ProgrammableNonFungible assets"
        )

    code = 153
    name = "InstructionNotSupported"
    msg = "Instruction not supported for ProgrammableNonFungible assets"


class KeyMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(154, "Public key does not match expected value")

    code = 154
    name = "KeyMismatch"
    msg = "Public key does not match expected value"


class LockedToken(ProgramError):
    def __init__(self) -> None:
        super().__init__(155, "Token is locked")

    code = 155
    name = "LockedToken"
    msg = "Token is locked"


class UnlockedToken(ProgramError):
    def __init__(self) -> None:
        super().__init__(156, "Token is unlocked")

    code = 156
    name = "UnlockedToken"
    msg = "Token is unlocked"


class MissingDelegateRole(ProgramError):
    def __init__(self) -> None:
        super().__init__(157, "Missing delegate role")

    code = 157
    name = "MissingDelegateRole"
    msg = "Missing delegate role"


class InvalidAuthorityType(ProgramError):
    def __init__(self) -> None:
        super().__init__(158, "Invalid authority type")

    code = 158
    name = "InvalidAuthorityType"
    msg = "Invalid authority type"


class MissingTokenRecord(ProgramError):
    def __init__(self) -> None:
        super().__init__(159, "Missing token record account")

    code = 159
    name = "MissingTokenRecord"
    msg = "Missing token record account"


class MintSupplyMustBeZero(ProgramError):
    def __init__(self) -> None:
        super().__init__(160, "Mint supply must be zero for programmable assets")

    code = 160
    name = "MintSupplyMustBeZero"
    msg = "Mint supply must be zero for programmable assets"


class DataIsEmptyOrZeroed(ProgramError):
    def __init__(self) -> None:
        super().__init__(161, "Data is empty or zeroed")

    code = 161
    name = "DataIsEmptyOrZeroed"
    msg = "Data is empty or zeroed"


class MissingTokenOwnerAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(162, "Missing token owner")

    code = 162
    name = "MissingTokenOwnerAccount"
    msg = "Missing token owner"


class InvalidMasterEditionAccountLength(ProgramError):
    def __init__(self) -> None:
        super().__init__(163, "Master edition account has an invalid length")

    code = 163
    name = "InvalidMasterEditionAccountLength"
    msg = "Master edition account has an invalid length"


class IncorrectTokenState(ProgramError):
    def __init__(self) -> None:
        super().__init__(164, "Incorrect token state")

    code = 164
    name = "IncorrectTokenState"
    msg = "Incorrect token state"


class InvalidDelegateRole(ProgramError):
    def __init__(self) -> None:
        super().__init__(165, "Invalid delegate role")

    code = 165
    name = "InvalidDelegateRole"
    msg = "Invalid delegate role"


class MissingPrintSupply(ProgramError):
    def __init__(self) -> None:
        super().__init__(166, "Print supply is required for non-fungibles")

    code = 166
    name = "MissingPrintSupply"
    msg = "Print supply is required for non-fungibles"


class MissingMasterEditionAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(167, "Missing master edition account")

    code = 167
    name = "MissingMasterEditionAccount"
    msg = "Missing master edition account"


class AmountMustBeGreaterThanZero(ProgramError):
    def __init__(self) -> None:
        super().__init__(168, "Amount must be greater than zero")

    code = 168
    name = "AmountMustBeGreaterThanZero"
    msg = "Amount must be greater than zero"


class InvalidDelegateArgs(ProgramError):
    def __init__(self) -> None:
        super().__init__(169, "Invalid delegate args")

    code = 169
    name = "InvalidDelegateArgs"
    msg = "Invalid delegate args"


class MissingLockedTransferAddress(ProgramError):
    def __init__(self) -> None:
        super().__init__(170, "Missing address for locked transfer")

    code = 170
    name = "MissingLockedTransferAddress"
    msg = "Missing address for locked transfer"


class InvalidLockedTransferAddress(ProgramError):
    def __init__(self) -> None:
        super().__init__(171, "Invalid destination address for locked transfer")

    code = 171
    name = "InvalidLockedTransferAddress"
    msg = "Invalid destination address for locked transfer"


class DataIncrementLimitExceeded(ProgramError):
    def __init__(self) -> None:
        super().__init__(172, "Exceeded account realloc increase limit")

    code = 172
    name = "DataIncrementLimitExceeded"
    msg = "Exceeded account realloc increase limit"


class CannotUpdateAssetWithDelegate(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            173,
            "Cannot update the rule set of a programmable asset that has a delegate",
        )

    code = 173
    name = "CannotUpdateAssetWithDelegate"
    msg = "Cannot update the rule set of a programmable asset that has a delegate"


class InvalidAmount(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            174, "Invalid token amount for this operation or token standard"
        )

    code = 174
    name = "InvalidAmount"
    msg = "Invalid token amount for this operation or token standard"


class MissingMasterEditionMintAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(175, "Missing master edition mint account")

    code = 175
    name = "MissingMasterEditionMintAccount"
    msg = "Missing master edition mint account"


class MissingMasterEditionTokenAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(176, "Missing master edition token account")

    code = 176
    name = "MissingMasterEditionTokenAccount"
    msg = "Missing master edition token account"


class MissingEditionMarkerAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(177, "Missing edition marker account")

    code = 177
    name = "MissingEditionMarkerAccount"
    msg = "Missing edition marker account"


class CannotBurnWithDelegate(ProgramError):
    def __init__(self) -> None:
        super().__init__(178, "Cannot burn while persistent delegate is set")

    code = 178
    name = "CannotBurnWithDelegate"
    msg = "Cannot burn while persistent delegate is set"


class MissingEdition(ProgramError):
    def __init__(self) -> None:
        super().__init__(179, "Missing edition account")

    code = 179
    name = "MissingEdition"
    msg = "Missing edition account"


class InvalidAssociatedTokenAccountProgram(ProgramError):
    def __init__(self) -> None:
        super().__init__(180, "Invalid Associated Token Account Program")

    code = 180
    name = "InvalidAssociatedTokenAccountProgram"
    msg = "Invalid Associated Token Account Program"


class InvalidInstructionsSysvar(ProgramError):
    def __init__(self) -> None:
        super().__init__(181, "Invalid InstructionsSysvar")

    code = 181
    name = "InvalidInstructionsSysvar"
    msg = "Invalid InstructionsSysvar"


class InvalidParentAccounts(ProgramError):
    def __init__(self) -> None:
        super().__init__(182, "Invalid or Unneeded parent accounts")

    code = 182
    name = "InvalidParentAccounts"
    msg = "Invalid or Unneeded parent accounts"


class InvalidUpdateArgs(ProgramError):
    def __init__(self) -> None:
        super().__init__(183, "Authority cannot apply all update args")

    code = 183
    name = "InvalidUpdateArgs"
    msg = "Authority cannot apply all update args"


class InsufficientTokenBalance(ProgramError):
    def __init__(self) -> None:
        super().__init__(184, "Token account does not have enough tokens")

    code = 184
    name = "InsufficientTokenBalance"
    msg = "Token account does not have enough tokens"


class MissingCollectionMint(ProgramError):
    def __init__(self) -> None:
        super().__init__(185, "Missing collection account")

    code = 185
    name = "MissingCollectionMint"
    msg = "Missing collection account"


class MissingCollectionMasterEdition(ProgramError):
    def __init__(self) -> None:
        super().__init__(186, "Missing collection master edition account")

    code = 186
    name = "MissingCollectionMasterEdition"
    msg = "Missing collection master edition account"


class InvalidTokenRecord(ProgramError):
    def __init__(self) -> None:
        super().__init__(187, "Invalid token record account")

    code = 187
    name = "InvalidTokenRecord"
    msg = "Invalid token record account"


class InvalidCloseAuthority(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            188, "The close authority needs to be revoked by the Utility Delegate"
        )

    code = 188
    name = "InvalidCloseAuthority"
    msg = "The close authority needs to be revoked by the Utility Delegate"


class InvalidInstruction(ProgramError):
    def __init__(self) -> None:
        super().__init__(189, "Invalid or removed instruction")

    code = 189
    name = "InvalidInstruction"
    msg = "Invalid or removed instruction"


class MissingDelegateRecord(ProgramError):
    def __init__(self) -> None:
        super().__init__(190, "Missing delegate record")

    code = 190
    name = "MissingDelegateRecord"
    msg = "Missing delegate record"


class InvalidFeeAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(191, "")

    code = 191
    name = "InvalidFeeAccount"
    msg = ""


class InvalidMetadataFlags(ProgramError):
    def __init__(self) -> None:
        super().__init__(192, "")

    code = 192
    name = "InvalidMetadataFlags"
    msg = ""


class CannotChangeUpdateAuthorityWithDelegate(ProgramError):
    def __init__(self) -> None:
        super().__init__(193, "Cannot change the update authority with a delegate")

    code = 193
    name = "CannotChangeUpdateAuthorityWithDelegate"
    msg = "Cannot change the update authority with a delegate"


class InvalidMintExtensionType(ProgramError):
    def __init__(self) -> None:
        super().__init__(194, "Invalid mint extension type")

    code = 194
    name = "InvalidMintExtensionType"
    msg = "Invalid mint extension type"


class InvalidMintCloseAuthority(ProgramError):
    def __init__(self) -> None:
        super().__init__(195, "Invalid mint close authority")

    code = 195
    name = "InvalidMintCloseAuthority"
    msg = "Invalid mint close authority"


class InvalidMetadataPointer(ProgramError):
    def __init__(self) -> None:
        super().__init__(196, "Invalid metadata pointer")

    code = 196
    name = "InvalidMetadataPointer"
    msg = "Invalid metadata pointer"


class InvalidTokenExtensionType(ProgramError):
    def __init__(self) -> None:
        super().__init__(197, "Invalid token extension type")

    code = 197
    name = "InvalidTokenExtensionType"
    msg = "Invalid token extension type"


class MissingImmutableOwnerExtension(ProgramError):
    def __init__(self) -> None:
        super().__init__(198, "Missing immutable owner extension")

    code = 198
    name = "MissingImmutableOwnerExtension"
    msg = "Missing immutable owner extension"


class ExpectedUninitializedAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(199, "Expected account to be uninitialized")

    code = 199
    name = "ExpectedUninitializedAccount"
    msg = "Expected account to be uninitialized"


class InvalidEditionAccountLength(ProgramError):
    def __init__(self) -> None:
        super().__init__(200, "Edition account has an invalid length")

    code = 200
    name = "InvalidEditionAccountLength"
    msg = "Edition account has an invalid length"


class AccountAlreadyResized(ProgramError):
    def __init__(self) -> None:
        super().__init__(201, "Account has already been resized")

    code = 201
    name = "AccountAlreadyResized"
    msg = "Account has already been resized"


class ConditionsForClosingNotMet(ProgramError):
    def __init__(self) -> None:
        super().__init__(202, "Conditions for closing not met")

    code = 202
    name = "ConditionsForClosingNotMet"
    msg = "Conditions for closing not met"


CustomError = typing.Union[
    InstructionUnpackError,
    InstructionPackError,
    NotRentExempt,
    AlreadyInitialized,
    Uninitialized,
    InvalidMetadataKey,
    InvalidEditionKey,
    UpdateAuthorityIncorrect,
    UpdateAuthorityIsNotSigner,
    NotMintAuthority,
    InvalidMintAuthority,
    NameTooLong,
    SymbolTooLong,
    UriTooLong,
    UpdateAuthorityMustBeEqualToMetadataAuthorityAndSigner,
    MintMismatch,
    EditionsMustHaveExactlyOneToken,
    MaxEditionsMintedAlready,
    TokenMintToFailed,
    MasterRecordMismatch,
    DestinationMintMismatch,
    EditionAlreadyMinted,
    PrintingMintDecimalsShouldBeZero,
    OneTimePrintingAuthorizationMintDecimalsShouldBeZero,
    EditionMintDecimalsShouldBeZero,
    TokenBurnFailed,
    TokenAccountOneTimeAuthMintMismatch,
    DerivedKeyInvalid,
    PrintingMintMismatch,
    OneTimePrintingAuthMintMismatch,
    TokenAccountMintMismatch,
    TokenAccountMintMismatchV2,
    NotEnoughTokens,
    PrintingMintAuthorizationAccountMismatch,
    AuthorizationTokenAccountOwnerMismatch,
    Disabled,
    CreatorsTooLong,
    CreatorsMustBeAtleastOne,
    MustBeOneOfCreators,
    NoCreatorsPresentOnMetadata,
    CreatorNotFound,
    InvalidBasisPoints,
    PrimarySaleCanOnlyBeFlippedToTrue,
    OwnerMismatch,
    NoBalanceInAccountForAuthorization,
    ShareTotalMustBe100,
    ReservationExists,
    ReservationDoesNotExist,
    ReservationNotSet,
    ReservationAlreadyMade,
    BeyondMaxAddressSize,
    NumericalOverflowError,
    ReservationBreachesMaximumSupply,
    AddressNotInReservation,
    CannotVerifyAnotherCreator,
    CannotUnverifyAnotherCreator,
    SpotMismatch,
    IncorrectOwner,
    PrintingWouldBreachMaximumSupply,
    DataIsImmutable,
    DuplicateCreatorAddress,
    ReservationSpotsRemainingShouldMatchTotalSpotsAtStart,
    InvalidTokenProgram,
    DataTypeMismatch,
    BeyondAlottedAddressSize,
    ReservationNotComplete,
    TriedToReplaceAnExistingReservation,
    InvalidOperation,
    InvalidOwner,
    PrintingMintSupplyMustBeZeroForConversion,
    OneTimeAuthMintSupplyMustBeZeroForConversion,
    InvalidEditionIndex,
    ReservationArrayShouldBeSizeOne,
    IsMutableCanOnlyBeFlippedToFalse,
    CollectionCannotBeVerifiedInThisInstruction,
    Removed,
    MustBeBurned,
    InvalidUseMethod,
    CannotChangeUseMethodAfterFirstUse,
    CannotChangeUsesAfterFirstUse,
    CollectionNotFound,
    InvalidCollectionUpdateAuthority,
    CollectionMustBeAUniqueMasterEdition,
    UseAuthorityRecordAlreadyExists,
    UseAuthorityRecordAlreadyRevoked,
    Unusable,
    NotEnoughUses,
    CollectionAuthorityRecordAlreadyExists,
    CollectionAuthorityDoesNotExist,
    InvalidUseAuthorityRecord,
    InvalidCollectionAuthorityRecord,
    InvalidFreezeAuthority,
    InvalidDelegate,
    CannotAdjustVerifiedCreator,
    CannotRemoveVerifiedCreator,
    CannotWipeVerifiedCreators,
    NotAllowedToChangeSellerFeeBasisPoints,
    EditionOverrideCannotBeZero,
    InvalidUser,
    RevokeCollectionAuthoritySignerIncorrect,
    TokenCloseFailed,
    UnsizedCollection,
    SizedCollection,
    MissingCollectionMetadata,
    NotAMemberOfCollection,
    NotVerifiedMemberOfCollection,
    NotACollectionParent,
    CouldNotDetermineTokenStandard,
    MissingEditionAccount,
    NotAMasterEdition,
    MasterEditionHasPrints,
    BorshDeserializationError,
    CannotUpdateVerifiedCollection,
    CollectionMasterEditionAccountInvalid,
    AlreadyVerified,
    AlreadyUnverified,
    NotAPrintEdition,
    InvalidMasterEdition,
    InvalidPrintEdition,
    InvalidEditionMarker,
    ReservationListDeprecated,
    PrintEditionDoesNotMatchMasterEdition,
    EditionNumberGreaterThanMaxSupply,
    MustUnverify,
    InvalidEscrowBumpSeed,
    MustBeEscrowAuthority,
    InvalidSystemProgram,
    MustBeNonFungible,
    InsufficientTokens,
    BorshSerializationError,
    NoFreezeAuthoritySet,
    InvalidCollectionSizeChange,
    InvalidBubblegumSigner,
    EscrowParentHasDelegate,
    MintIsNotSigner,
    InvalidTokenStandard,
    InvalidMintForTokenStandard,
    InvalidAuthorizationRules,
    MissingAuthorizationRules,
    MissingProgrammableConfig,
    InvalidProgrammableConfig,
    DelegateAlreadyExists,
    DelegateNotFound,
    MissingAccountInBuilder,
    MissingArgumentInBuilder,
    FeatureNotSupported,
    InvalidSystemWallet,
    OnlySaleDelegateCanTransfer,
    MissingTokenAccount,
    MissingSplTokenProgram,
    MissingAuthorizationRulesProgram,
    InvalidDelegateRoleForTransfer,
    InvalidTransferAuthority,
    InstructionNotSupported,
    KeyMismatch,
    LockedToken,
    UnlockedToken,
    MissingDelegateRole,
    InvalidAuthorityType,
    MissingTokenRecord,
    MintSupplyMustBeZero,
    DataIsEmptyOrZeroed,
    MissingTokenOwnerAccount,
    InvalidMasterEditionAccountLength,
    IncorrectTokenState,
    InvalidDelegateRole,
    MissingPrintSupply,
    MissingMasterEditionAccount,
    AmountMustBeGreaterThanZero,
    InvalidDelegateArgs,
    MissingLockedTransferAddress,
    InvalidLockedTransferAddress,
    DataIncrementLimitExceeded,
    CannotUpdateAssetWithDelegate,
    InvalidAmount,
    MissingMasterEditionMintAccount,
    MissingMasterEditionTokenAccount,
    MissingEditionMarkerAccount,
    CannotBurnWithDelegate,
    MissingEdition,
    InvalidAssociatedTokenAccountProgram,
    InvalidInstructionsSysvar,
    InvalidParentAccounts,
    InvalidUpdateArgs,
    InsufficientTokenBalance,
    MissingCollectionMint,
    MissingCollectionMasterEdition,
    InvalidTokenRecord,
    InvalidCloseAuthority,
    InvalidInstruction,
    MissingDelegateRecord,
    InvalidFeeAccount,
    InvalidMetadataFlags,
    CannotChangeUpdateAuthorityWithDelegate,
    InvalidMintExtensionType,
    InvalidMintCloseAuthority,
    InvalidMetadataPointer,
    InvalidTokenExtensionType,
    MissingImmutableOwnerExtension,
    ExpectedUninitializedAccount,
    InvalidEditionAccountLength,
    AccountAlreadyResized,
    ConditionsForClosingNotMet,
]
CUSTOM_ERROR_MAP: dict[int, CustomError] = {
    0: InstructionUnpackError(),
    1: InstructionPackError(),
    2: NotRentExempt(),
    3: AlreadyInitialized(),
    4: Uninitialized(),
    5: InvalidMetadataKey(),
    6: InvalidEditionKey(),
    7: UpdateAuthorityIncorrect(),
    8: UpdateAuthorityIsNotSigner(),
    9: NotMintAuthority(),
    10: InvalidMintAuthority(),
    11: NameTooLong(),
    12: SymbolTooLong(),
    13: UriTooLong(),
    14: UpdateAuthorityMustBeEqualToMetadataAuthorityAndSigner(),
    15: MintMismatch(),
    16: EditionsMustHaveExactlyOneToken(),
    17: MaxEditionsMintedAlready(),
    18: TokenMintToFailed(),
    19: MasterRecordMismatch(),
    20: DestinationMintMismatch(),
    21: EditionAlreadyMinted(),
    22: PrintingMintDecimalsShouldBeZero(),
    23: OneTimePrintingAuthorizationMintDecimalsShouldBeZero(),
    24: EditionMintDecimalsShouldBeZero(),
    25: TokenBurnFailed(),
    26: TokenAccountOneTimeAuthMintMismatch(),
    27: DerivedKeyInvalid(),
    28: PrintingMintMismatch(),
    29: OneTimePrintingAuthMintMismatch(),
    30: TokenAccountMintMismatch(),
    31: TokenAccountMintMismatchV2(),
    32: NotEnoughTokens(),
    33: PrintingMintAuthorizationAccountMismatch(),
    34: AuthorizationTokenAccountOwnerMismatch(),
    35: Disabled(),
    36: CreatorsTooLong(),
    37: CreatorsMustBeAtleastOne(),
    38: MustBeOneOfCreators(),
    39: NoCreatorsPresentOnMetadata(),
    40: CreatorNotFound(),
    41: InvalidBasisPoints(),
    42: PrimarySaleCanOnlyBeFlippedToTrue(),
    43: OwnerMismatch(),
    44: NoBalanceInAccountForAuthorization(),
    45: ShareTotalMustBe100(),
    46: ReservationExists(),
    47: ReservationDoesNotExist(),
    48: ReservationNotSet(),
    49: ReservationAlreadyMade(),
    50: BeyondMaxAddressSize(),
    51: NumericalOverflowError(),
    52: ReservationBreachesMaximumSupply(),
    53: AddressNotInReservation(),
    54: CannotVerifyAnotherCreator(),
    55: CannotUnverifyAnotherCreator(),
    56: SpotMismatch(),
    57: IncorrectOwner(),
    58: PrintingWouldBreachMaximumSupply(),
    59: DataIsImmutable(),
    60: DuplicateCreatorAddress(),
    61: ReservationSpotsRemainingShouldMatchTotalSpotsAtStart(),
    62: InvalidTokenProgram(),
    63: DataTypeMismatch(),
    64: BeyondAlottedAddressSize(),
    65: ReservationNotComplete(),
    66: TriedToReplaceAnExistingReservation(),
    67: InvalidOperation(),
    68: InvalidOwner(),
    69: PrintingMintSupplyMustBeZeroForConversion(),
    70: OneTimeAuthMintSupplyMustBeZeroForConversion(),
    71: InvalidEditionIndex(),
    72: ReservationArrayShouldBeSizeOne(),
    73: IsMutableCanOnlyBeFlippedToFalse(),
    74: CollectionCannotBeVerifiedInThisInstruction(),
    75: Removed(),
    76: MustBeBurned(),
    77: InvalidUseMethod(),
    78: CannotChangeUseMethodAfterFirstUse(),
    79: CannotChangeUsesAfterFirstUse(),
    80: CollectionNotFound(),
    81: InvalidCollectionUpdateAuthority(),
    82: CollectionMustBeAUniqueMasterEdition(),
    83: UseAuthorityRecordAlreadyExists(),
    84: UseAuthorityRecordAlreadyRevoked(),
    85: Unusable(),
    86: NotEnoughUses(),
    87: CollectionAuthorityRecordAlreadyExists(),
    88: CollectionAuthorityDoesNotExist(),
    89: InvalidUseAuthorityRecord(),
    90: InvalidCollectionAuthorityRecord(),
    91: InvalidFreezeAuthority(),
    92: InvalidDelegate(),
    93: CannotAdjustVerifiedCreator(),
    94: CannotRemoveVerifiedCreator(),
    95: CannotWipeVerifiedCreators(),
    96: NotAllowedToChangeSellerFeeBasisPoints(),
    97: EditionOverrideCannotBeZero(),
    98: InvalidUser(),
    99: RevokeCollectionAuthoritySignerIncorrect(),
    100: TokenCloseFailed(),
    101: UnsizedCollection(),
    102: SizedCollection(),
    103: MissingCollectionMetadata(),
    104: NotAMemberOfCollection(),
    105: NotVerifiedMemberOfCollection(),
    106: NotACollectionParent(),
    107: CouldNotDetermineTokenStandard(),
    108: MissingEditionAccount(),
    109: NotAMasterEdition(),
    110: MasterEditionHasPrints(),
    111: BorshDeserializationError(),
    112: CannotUpdateVerifiedCollection(),
    113: CollectionMasterEditionAccountInvalid(),
    114: AlreadyVerified(),
    115: AlreadyUnverified(),
    116: NotAPrintEdition(),
    117: InvalidMasterEdition(),
    118: InvalidPrintEdition(),
    119: InvalidEditionMarker(),
    120: ReservationListDeprecated(),
    121: PrintEditionDoesNotMatchMasterEdition(),
    122: EditionNumberGreaterThanMaxSupply(),
    123: MustUnverify(),
    124: InvalidEscrowBumpSeed(),
    125: MustBeEscrowAuthority(),
    126: InvalidSystemProgram(),
    127: MustBeNonFungible(),
    128: InsufficientTokens(),
    129: BorshSerializationError(),
    130: NoFreezeAuthoritySet(),
    131: InvalidCollectionSizeChange(),
    132: InvalidBubblegumSigner(),
    133: EscrowParentHasDelegate(),
    134: MintIsNotSigner(),
    135: InvalidTokenStandard(),
    136: InvalidMintForTokenStandard(),
    137: InvalidAuthorizationRules(),
    138: MissingAuthorizationRules(),
    139: MissingProgrammableConfig(),
    140: InvalidProgrammableConfig(),
    141: DelegateAlreadyExists(),
    142: DelegateNotFound(),
    143: MissingAccountInBuilder(),
    144: MissingArgumentInBuilder(),
    145: FeatureNotSupported(),
    146: InvalidSystemWallet(),
    147: OnlySaleDelegateCanTransfer(),
    148: MissingTokenAccount(),
    149: MissingSplTokenProgram(),
    150: MissingAuthorizationRulesProgram(),
    151: InvalidDelegateRoleForTransfer(),
    152: InvalidTransferAuthority(),
    153: InstructionNotSupported(),
    154: KeyMismatch(),
    155: LockedToken(),
    156: UnlockedToken(),
    157: MissingDelegateRole(),
    158: InvalidAuthorityType(),
    159: MissingTokenRecord(),
    160: MintSupplyMustBeZero(),
    161: DataIsEmptyOrZeroed(),
    162: MissingTokenOwnerAccount(),
    163: InvalidMasterEditionAccountLength(),
    164: IncorrectTokenState(),
    165: InvalidDelegateRole(),
    166: MissingPrintSupply(),
    167: MissingMasterEditionAccount(),
    168: AmountMustBeGreaterThanZero(),
    169: InvalidDelegateArgs(),
    170: MissingLockedTransferAddress(),
    171: InvalidLockedTransferAddress(),
    172: DataIncrementLimitExceeded(),
    173: CannotUpdateAssetWithDelegate(),
    174: InvalidAmount(),
    175: MissingMasterEditionMintAccount(),
    176: MissingMasterEditionTokenAccount(),
    177: MissingEditionMarkerAccount(),
    178: CannotBurnWithDelegate(),
    179: MissingEdition(),
    180: InvalidAssociatedTokenAccountProgram(),
    181: InvalidInstructionsSysvar(),
    182: InvalidParentAccounts(),
    183: InvalidUpdateArgs(),
    184: InsufficientTokenBalance(),
    185: MissingCollectionMint(),
    186: MissingCollectionMasterEdition(),
    187: InvalidTokenRecord(),
    188: InvalidCloseAuthority(),
    189: InvalidInstruction(),
    190: MissingDelegateRecord(),
    191: InvalidFeeAccount(),
    192: InvalidMetadataFlags(),
    193: CannotChangeUpdateAuthorityWithDelegate(),
    194: InvalidMintExtensionType(),
    195: InvalidMintCloseAuthority(),
    196: InvalidMetadataPointer(),
    197: InvalidTokenExtensionType(),
    198: MissingImmutableOwnerExtension(),
    199: ExpectedUninitializedAccount(),
    200: InvalidEditionAccountLength(),
    201: AccountAlreadyResized(),
    202: ConditionsForClosingNotMet(),
}


def from_code(code: int) -> typing.Optional[CustomError]:
    maybe_err = CUSTOM_ERROR_MAP.get(code)
    if maybe_err is None:
        return None
    return maybe_err
